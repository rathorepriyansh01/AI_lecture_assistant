"""
=========================================================
AI Lecture Assistant
Frontend Settings
=========================================================

Central configuration for the Streamlit frontend.
"""

import os
from dotenv import load_dotenv

# =========================================================
# Load Environment
# =========================================================

load_dotenv()

# =========================================================
# Application
# =========================================================

APP_NAME = "AI Lecture Assistant"

APP_VERSION = "1.0.0"

# =========================================================
# FastAPI Backend
# =========================================================

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        120
    )
)

# =========================================================
# Upload
# =========================================================

MAX_UPLOAD_SIZE_MB = int(
    os.getenv(
        "MAX_UPLOAD_SIZE_MB",
        2048
    )
)

SUPPORTED_VIDEO_FORMATS = [

    "mp4",

    "mkv",

    "avi",

    "mov",

    "webm"

]

# =========================================================
# UI
# =========================================================

DEFAULT_THEME = "dark"

DEFAULT_PAGE = "Dashboard"