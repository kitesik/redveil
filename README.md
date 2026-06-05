# Redveil

Redveil detects faces in photos and covers each face with a red privacy grid. It is built for quick local defacing: a command-line tool for files or folders, plus a small FastAPI endpoint for upload workflows.

The visual style is inspired by the red face veils often seen in AI video workflows, where creators want a clear, repeatable privacy layer over reference faces before sharing previews or datasets.

Redveil is a privacy aid, not a guarantee or a moderation-bypass tool. Face detectors can miss faces, side profiles, low-light photos, masks, or stylized images. Review output before publishing sensitive images, and follow the policies of any platform where the output is uploaded.

## 한국어

Redveil은 AI 레퍼런스 이미지, AI 영상 생성 워크플로, 프리비주얼 영상, 데이터셋 샘플, 튜토리얼 캡처에서 얼굴 사진을 붉은 격자 베일로 가리는 얼굴 익명화 도구입니다. 얼굴 위에 red face grid, red face veil, red privacy mask를 씌워 원본 얼굴 식별성을 줄이는 데 초점을 둡니다.

이 프로젝트는 플랫폼 규정이나 업로드 제한을 우회하기 위한 도구가 아닙니다. 사람 얼굴, 레퍼런스 이미지, 초상권이 포함된 자료를 다룰 때는 본인 동의, 공개 범위, 서비스 정책, 지역 법규를 확인해야 합니다.

검색 키워드: 레드페이스, 붉은 얼굴 격자, 얼굴 익명화, 얼굴 비식별화, AI 레퍼런스 이미지 프라이버시, AI 영상 생성 얼굴 보호, reference face privacy, red face veil, red face grid, face anonymization, face de-identification, privacy mask, OpenCV face redaction, FastAPI deface API.

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

## Deploy

This repository includes a Vercel-compatible FastAPI entrypoint:

```bash
vercel --prod
```

## Development

```bash
ruff check .
pytest
```
