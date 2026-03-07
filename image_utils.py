# HEIC 변환, 원본 바이너리 추출, 리사이즈 유틸리티 — Streamlit 업로드 이미지 처리
from __future__ import annotations

import io
import os

from PIL import Image

from config import MAX_LONG_EDGE

# 확장자 → MIME type 매핑 (Streamlit이 MIME을 잘못 감지할 때 fallback)
_EXT_TO_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".heic": "image/heic",
    ".heif": "image/heif",
}

# pillow-heif가 설치되어 있으면 등록
try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False


def get_raw_image_bytes(uploaded_file) -> tuple:
    """Streamlit UploadedFile에서 원본 바이너리와 MIME type 추출 (나노바나나 동일 방식)

    나노바나나 MCP는 파일을 open(path, "rb").read()로 원본 그대로 읽음.
    웹앱도 동일하게 원본 바이너리를 보존하여 API에 전달.
    HEIC/HEIF만 JPEG로 변환 (Gemini API HEIC 지원 불확실).

    Returns:
        (raw_bytes, mime_type) 튜플
    """
    raw_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or ""

    # Streamlit Cloud에서 MIME이 application/octet-stream 등 비정상일 때
    # → 파일 확장자로 MIME 추론
    if not mime_type.startswith("image/"):
        ext = os.path.splitext(uploaded_file.name)[1].lower() if uploaded_file.name else ""
        mime_type = _EXT_TO_MIME.get(ext, "image/jpeg")  # 최종 fallback: JPEG

    # HEIC/HEIF → JPEG 변환 (Gemini API 호환성)
    if "heic" in mime_type.lower() or "heif" in mime_type.lower():
        img = Image.open(io.BytesIO(raw_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        return buf.getvalue(), "image/jpeg"

    return raw_bytes, mime_type


def process_uploaded_image(uploaded_file) -> Image.Image:
    """Streamlit UploadedFile -> PIL Image (RGB, 리사이즈) — UI 미리보기 전용"""
    image = Image.open(uploaded_file)
    if image.mode != "RGB":
        image = image.convert("RGB")
    w, h = image.size
    if max(w, h) > MAX_LONG_EDGE:
        ratio = MAX_LONG_EDGE / max(w, h)
        image = image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    return image


def image_to_bytes(image: Image.Image, format: str = "JPEG", quality: int = 90) -> bytes:
    """PIL Image -> bytes"""
    buf = io.BytesIO()
    image.save(buf, format=format, quality=quality)
    return buf.getvalue()
