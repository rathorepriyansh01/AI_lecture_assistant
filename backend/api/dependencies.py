"""
=========================================================
AI Lecture Assistant
Dependencies
=========================================================
"""

from functools import lru_cache

from backend.services.summary_service import SummaryService
from backend.services.notes_service import NotesService
from backend.services.quiz_service import QuizService
from backend.services.chatbot_service import ChatbotService


# ==========================================================
# Summary Service
# ==========================================================

@lru_cache(maxsize=1)
def get_summary_service():

    return SummaryService()


# ==========================================================
# Notes Service
# ==========================================================

@lru_cache(maxsize=1)
def get_notes_service():

    return NotesService()


# ==========================================================
# Quiz Service
# ==========================================================

@lru_cache(maxsize=1)
def get_quiz_service():

    return QuizService()


# ==========================================================
# Chat Service
# ==========================================================

@lru_cache(maxsize=1)
def get_chat_service():

    return ChatbotService()

from backend.services.videoupload_service import VideoService


@lru_cache(maxsize=1)
def get_upload_service():

    return VideoService()

from backend.utils.metadata_manager import MetadataManager


@lru_cache(maxsize=1)
def get_metadata_service():

    return MetadataManager()