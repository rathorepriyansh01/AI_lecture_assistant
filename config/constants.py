"""
=========================================================
Project Constants
=========================================================
"""

# ---------------------------------------------------------
# Supported Files
# ---------------------------------------------------------

VIDEO_EXTENSIONS = [

    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm"

]

AUDIO_EXTENSIONS = [

    ".mp3",
    ".wav",
    ".m4a"

]

# ---------------------------------------------------------
# Chunking
# ---------------------------------------------------------

CHUNK_DURATION = 25

OVERLAP_WORDS = 40

MIN_WORDS = 30

MAX_WORDS = 250

# ---------------------------------------------------------
# Language
# ---------------------------------------------------------

DEFAULT_LANGUAGE = "en"

# ---------------------------------------------------------
# Pipeline Status
# ---------------------------------------------------------

STATUS_UPLOADED = "Uploaded"

STATUS_AUDIO_READY = "Audio Ready"

STATUS_TRANSCRIBED = "Transcribed"

STATUS_CHUNKED = "Chunked"

STATUS_EMBEDDED = "Embedded"

STATUS_INDEXED = "Indexed"

STATUS_COMPLETED = "Completed"

STATUS_FAILED = "Failed"
