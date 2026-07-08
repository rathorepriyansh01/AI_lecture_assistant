"""
=========================================================
AI Lecture Assistant
Project Settings
=========================================================
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================================
# Load Environment
# ==========================================================

load_dotenv()

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==========================================================
# Directories
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

LECTURES_DIR = DATA_DIR / "lectures"

CHROMA_DB_DIR = DATA_DIR / "chroma_db"

CACHE_DIR = DATA_DIR / "cache"

EXPORT_DIR = DATA_DIR / "exports"

LOG_DIR = PROJECT_ROOT / "logs"

# Create directories

for folder in [

    DATA_DIR,

    LECTURES_DIR,

    CHROMA_DB_DIR,

    CACHE_DIR,

    EXPORT_DIR,

    LOG_DIR

]:

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

# ==========================================================
# Upload Settings
# ==========================================================

MAX_UPLOAD_SIZE_MB = 1024

# ==========================================================
# Whisper
# ==========================================================

WHISPER_MODEL = os.getenv(

    "WHISPER_MODEL",

    "small"

)

# ==========================================================
# Embedding
# ==========================================================

EMBEDDING_MODEL = os.getenv(

    "EMBEDDING_MODEL",

    "BAAI/bge-m3"

)

COLLECTION_NAME = os.getenv(

    "COLLECTION_NAME",

    "lecture_rag"

)

CHROMA_DB_PATH = str(

    CHROMA_DB_DIR

)

# ==========================================================
# Retrieval
# ==========================================================

TOP_K = int(

    os.getenv(

        "TOP_K",

        8

    )

)

SEARCH_K = int(

    os.getenv(

        "SEARCH_K",

        20

    )

)

SIMILARITY_THRESHOLD = None

MAX_CONTEXT_CHARS = int(

    os.getenv(

        "MAX_CONTEXT_CHARS",

        12000

    )

)

# ==========================================================
# API Keys
# ==========================================================

GEMINI_API_KEY = os.getenv(

    "GEMINI_API_KEY"

)

GROQ_API_KEY = os.getenv(

    "GROQ_API_KEY"

)

NVIDIA_API_KEY = os.getenv(

    "NVIDIA_API_KEY"

)

# ==========================================================
# Models
# ==========================================================

GEMINI_MODEL = os.getenv(

    "GEMINI_MODEL",

    "gemini-3.5-flash"

)

GROQ_MODEL = os.getenv(

    "GROQ_MODEL",

    "llama-3.3-70b-versatile"

)

NVIDIA_MODEL = os.getenv(

    "NVIDIA_MODEL",

    "mistralai/mistral-medium-3.5-128b"

)

# ==========================================================
# LLM
# ==========================================================

PRIMARY_PROVIDER = os.getenv(

    "PRIMARY_PROVIDER",

    "gemini"

).lower()

SECONDARY_PROVIDER = os.getenv(

    "SECONDARY_PROVIDER",

    "groq"

).lower()

THIRD_PROVIDER = os.getenv(

    "THIRD_PROVIDER",

    "nvidia"

).lower()

LLM_PROVIDER = PRIMARY_PROVIDER

TEMPERATURE = float(

    os.getenv(

        "TEMPERATURE",

        0.2

    )

)

MAX_TOKENS = int(

    os.getenv(

        "MAX_TOKENS",

        4096

    )

)

# ==========================================================
# Provider Retry
# ==========================================================

MAX_RETRY = int(

    os.getenv(

        "MAX_RETRY",

        2

    )

)

PROVIDER_COOLDOWN = int(

    os.getenv(

        "PROVIDER_COOLDOWN",

        300

    )

)

REQUEST_TIMEOUT = int(

    os.getenv(

        "REQUEST_TIMEOUT",

        120

    )

)

# ==========================================================
# Cache
# ==========================================================

ENABLE_CACHE = True

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = os.getenv(

    "LOG_LEVEL",

    "INFO"

)