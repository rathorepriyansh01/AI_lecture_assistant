"""
=========================================================
AI Lecture Assistant
Summary API
Production Version
=========================================================
"""

import logging

from api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class SummaryAPI(BaseAPIClient):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Generate Summary
    # =====================================================

    def generate(

        self,

        lecture_id,

        summary_type="short",

        use_cache=False

    ):

        payload = {

            "lecture_id": lecture_id,

            "summary_type": summary_type,

            "use_cache": use_cache

        }

        logger.info(

            f"Generating {summary_type} summary..."

        )

        return self.post(

            "/summary",

            json=payload

        )