# IR 프로필 웹앱 환경변수 및 상수 설정
import os
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3-pro-image-preview")
MAX_UPLOAD_SIZE_MB = 20
MAX_LONG_EDGE = 2048
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp"}
REFERENCE_DIR = os.path.join(os.path.dirname(__file__), "reference")
THUMBNAIL_DIR = os.path.join(os.path.dirname(__file__), "thumbnails")
