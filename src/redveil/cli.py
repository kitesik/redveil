from __future__ import annotations

import argparse
from pathlib import Path

from redveil.processor import RedveilOptions, process_file

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="redveil",
        description="Detect faces and cover them with a red privacy grid.",
    )
    parser.add_argument("input", type=Path, help="Input image file or directory.")
    parser.add_argument("output", type=Path, help="Output image file or directory.")
    parser.add_argument("--padding", type=float, default=0.16, help="Face box padding ratio.")
    parser.add_argument("--blur", type=int, default=37, help="Gaussian blur strength.")
    parser.add_argument("--grid-step", type=int, default=13, help="Grid spacing in pixels.")
    parser.add_argument("--line-width", type=int, default=2, help="Grid line width in pixels.")
    parser.add_argument("--alpha", type=float, default=0.78, help="Grid overlay opacity.")
    args = parser.parse_args()

    options = RedveilOptions(
        padding=args.padding,
        blur_strength=args.blur,
        grid_step=args.grid_step,
        line_width=args.line_width,
        alpha=args.alpha,
    )

    if args.input.is_dir():
        total = _process_directory(args.input, args.output, options)
        print(f"redveil: processed {total} image(s) into {args.output}")
        return

    faces = process_file(args.input, args.output, options)
    print(f"redveil: masked {faces} face(s) -> {args.output}")


def _process_directory(input_dir: Path, output_dir: Path, options: RedveilOptions) -> int:
    count = 0
    for input_path in sorted(input_dir.rglob("*")):
        if input_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        relative_path = input_path.relative_to(input_dir)
        output_path = output_dir / relative_path
        faces = process_file(input_path, output_path, options)
        print(f"redveil: {relative_path} masked {faces} face(s)")
        count += 1
    return count


if __name__ == "__main__":
    main()
