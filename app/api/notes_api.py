"""
=========================================================
AI Lecture Assistant
Notes API
=========================================================

Wrapper for Notes Endpoints
"""

import logging

from api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class NotesAPI(BaseAPIClient):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Generate Notes
    # =====================================================

    def generate(

        self,

        lecture_id,

        notes_type="detailed",

        use_cache=False

    ):

        payload = {

            "lecture_id": lecture_id,

            "notes_type": notes_type,

            "use_cache": use_cache

        }

        logger.info(

            f"Generating {notes_type} notes..."

        )

        return self.post(

            "/notes",

            json=payload

        )