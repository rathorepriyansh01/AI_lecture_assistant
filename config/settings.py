"""
=========================================================
AI Lecture Assistant
Project Settings
=========================================================
"""

from pathlib import Path
from dotenv import load_dotenv
import os

import groq
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# Data Directories
# ---------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

LECTURES_DIR = DATA_DIR / "lectures"

CHROMA_DB_DIR = DATA_DIR / "chroma_db"

CACHE_DIR = DATA_DIR / "cache"

EXPORT_DIR = DATA_DIR / "exports"

# ---------------------------------------------------------
# AI Models
# ---------------------------------------------------------

WHISPER_MODEL = "small"

EMBEDDING_MODEL = "bge-m3:latest"

LLM_MODEL = "llama-3.3-70b-versatile"



TOP_K = 8

# ---------------------------------------------------------
# Upload Settings
# ---------------------------------------------------------

MAX_UPLOAD_SIZE_MB = 1024

# =====================================================
# Retrieval Settings
# =====================================================

TOP_K = 8

SEARCH_K = 20

SIMILARITY_THRESHOLD = None

MAX_CONTEXT_CHARS = 12000
# ---------------------------------------------------------
# API Keys
# ---------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")


# ==========================================================
# Embedding
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-m3"

COLLECTION_NAME = "lecture_rag"

CHROMA_DB_PATH = str(

    DATA_DIR / "chroma_db"

)
TOP_K = 8

# =====================================================
# LLM
# =====================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"

PRIMARY_PROVIDER= os.getenv("PRIMARY_PROVIDER", "gemini")

TEMPERATURE = 0.2

MAX_TOKENS = 4096

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
SECONDARY_PROVIDER = os.getenv("SECONDARY_PROVIDER", "groq")
THIRD_PROVIDER = os.getenv("THIRD_PROVIDER", "nvidia")


NVIDIA_MODEL = os.getenv(

    "NVIDIA_MODEL",

    "deepseek-ai/deepseek-v4-flasht"

)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(

    "GEMINI_MODEL",

    "gemini-2.5-flash"

)


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "nvidia")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")


# ---------------------------------------------------------
# Create Required Directories
# ---------------------------------------------------------

for folder in [

    DATA_DIR,

    LECTURES_DIR,

    CHROMA_DB_DIR,

    CACHE_DIR,

    EXPORT_DIR

]:

    folder.mkdir(

        parents=True,

        exist_ok=True

    )
