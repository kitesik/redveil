# Redveil

Redveil detects faces in photos and covers each face with a red privacy grid. It is built for quick local defacing: a command-line tool for files or folders, plus a small FastAPI endpoint for upload workflows.

Redveil is a privacy aid, not a guarantee. Face detectors can miss faces, side profiles, low-light photos, masks, or stylized images. Review output before publishing sensitive images.

## Features

- Detects frontal faces with OpenCV's bundled Haar cascade.
- Adds optional blur under a red grid mask.
- Works as a CLI for single images or folders.
- Exposes a `/redveil` FastAPI endpoint that returns a PNG.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

```bash
redveil input.jpg output.png
redveil ./photos ./redveil-output --grid-step 12 --line-width 2 --blur 41
```

## API

```bash
uvicorn redveil.api:app --reload
```

Then upload an image:

```bash
curl -X POST "http://127.0.0.1:8000/redveil" \
  -F "file=@input.jpg" \
  --output redveil.png
```

OpenAPI docs are available at `http://127.0.0.1:8000/docs`.

## Development

```bash
ruff check .
pytest
```
