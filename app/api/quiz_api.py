"""
=========================================================
AI Lecture Assistant
Quiz API
=========================================================

Wrapper for Quiz Endpoints
"""

import logging

from api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class QuizAPI(BaseAPIClient):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Generate Quiz
    # =====================================================

    def generate(

        self,

        lecture_id,

        difficulty="medium",

        total_questions=20,

        use_cache=False

    ):

        payload = {

            "lecture_id": lecture_id,

            "difficulty": difficulty,

            "total_questions": total_questions,

            "use_cache": use_cache

        }

        logger.info(

            f"Generating {total_questions} {difficulty} questions..."

        )

        return self.post(

            "/quiz",

            json=payload

        )