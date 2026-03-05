# IR 프로필 웹앱 환경변수 및 상수 설정
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def _get_secret(key: str, default: str = "") -> str:
    """Streamlit Cloud: st.secrets 우선, 로컬: os.getenv fallback"""
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)


GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
MODEL_NAME = _get_secret("MODEL_NAME", "gemini-3-pro-image-preview")
MAX_UPLOAD_SIZE_MB = 20
MAX_LONG_EDGE = 2048
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "reference")
THUMBNAIL_DIR = os.path.join(os.path.dirname(__file__), "thumbnails")
