from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np


@dataclass(frozen=True)
class RedveilOptions:
    """Options for face redaction and the red grid overlay."""

    padding: float = 0.16
    blur_strength: int = 37
    grid_step: int = 13
    line_width: int = 2
    alpha: float = 0.78
    min_neighbors: int = 5
    scale_factor: float = 1.08


FaceBox = tuple[int, int, int, int]


def detect_faces(image_bgr: np.ndarray, options: RedveilOptions) -> list[FaceBox]:
    """Detect frontal faces with OpenCV's bundled Haar cascade."""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(str(cascade_path))
    if cascade.empty():
        raise RuntimeError(f"Could not load face cascade: {cascade_path}")

    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=options.scale_factor,
        minNeighbors=options.min_neighbors,
        minSize=(24, 24),
    )
    return [tuple(int(v) for v in face) for face in faces]


def process_image(image_bgr: np.ndarray, options: RedveilOptions | None = None) -> np.ndarray:
    """Return a copy of the image with detected faces covered by Redveil."""
    active_options = options or RedveilOptions()
    faces = detect_faces(image_bgr, active_options)
    return apply_redveil(image_bgr, faces, active_options)


def apply_redveil(
    image_bgr: np.ndarray,
    faces: Iterable[FaceBox],
    options: RedveilOptions | None = None,
) -> np.ndarray:
    """Apply red grid masking to known face boxes."""
    active_options = options or RedveilOptions()
    output = image_bgr.copy()

    for face in faces:
        x1, y1, x2, y2 = _expanded_box(face, output.shape, active_options.padding)
        roi = output[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        if active_options.blur_strength > 0:
            kernel = _odd_kernel(active_options.blur_strength)
            roi = cv2.GaussianBlur(roi, (kernel, kernel), 0)

        veil = roi.copy()
        veil[:, :] = _blend_with_red(veil)
        _draw_grid(veil, active_options.grid_step, active_options.line_width)
        output[y1:y2, x1:x2] = cv2.addWeighted(
            veil,
            active_options.alpha,
            roi,
            1.0 - active_options.alpha,
            0,
        )

    return output


def read_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return image


def write_image(path: Path, image_bgr: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), image_bgr)
    if not ok:
        raise ValueError(f"Could not write image: {path}")


def process_file(input_path: Path, output_path: Path, options: RedveilOptions) -> int:
    image = read_image(input_path)
    faces = detect_faces(image, options)
    write_image(output_path, apply_redveil(image, faces, options))
    return len(faces)


def _expanded_box(face: FaceBox, shape: tuple[int, ...], padding: float) -> FaceBox:
    x, y, w, h = face
    pad_x = int(w * padding)
    pad_y = int(h * padding)
    height, width = shape[:2]
    return (
        max(0, x - pad_x),
        max(0, y - pad_y),
        min(width, x + w + pad_x),
        min(height, y + h + pad_y),
    )


def _odd_kernel(value: int) -> int:
    kernel = max(1, int(value))
    return kernel if kernel % 2 == 1 else kernel + 1


def _blend_with_red(image_bgr: np.ndarray) -> np.ndarray:
    red_layer = np.zeros_like(image_bgr)
    red_layer[:, :, 2] = 255
    return cv2.addWeighted(image_bgr, 0.35, red_layer, 0.65, 0)


def _draw_grid(image_bgr: np.ndarray, grid_step: int, line_width: int) -> None:
    step = max(4, int(grid_step))
    thickness = max(1, int(line_width))
    height, width = image_bgr.shape[:2]
    line_color = (0, 0, 255)
    glow_color = (30, 30, 255)

    for x in range(0, width, step):
        cv2.line(image_bgr, (x, 0), (x, height), glow_color, thickness + 2)
        cv2.line(image_bgr, (x, 0), (x, height), line_color, thickness)
    for y in range(0, height, step):
        cv2.line(image_bgr, (0, y), (width, y), glow_color, thickness + 2)
        cv2.line(image_bgr, (0, y), (width, y), line_color, thickness)
