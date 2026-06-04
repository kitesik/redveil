from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response

from redveil.processor import RedveilOptions, process_image

app = FastAPI(
    title="Redveil API",
    description="Upload an image and receive a copy with detected faces covered by a red grid.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/redveil")
async def redveil(
    file: UploadFile = File(...),
    padding: float = 0.16,
    blur: int = 37,
    grid_step: int = 13,
    line_width: int = 2,
    alpha: float = 0.78,
) -> Response:
    raw = await file.read()
    image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return Response("Could not decode image.", status_code=400)

    options = RedveilOptions(
        padding=padding,
        blur_strength=blur,
        grid_step=grid_step,
        line_width=line_width,
        alpha=alpha,
    )
    processed = process_image(image, options)
    ok, encoded = cv2.imencode(".png", processed)
    if not ok:
        return Response("Could not encode image.", status_code=500)

    return Response(
        BytesIO(encoded.tobytes()).getvalue(),
        media_type="image/png",
        headers={"Content-Disposition": 'attachment; filename="redveil.png"'},
    )
