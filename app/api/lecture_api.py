"""
=========================================================
AI Lecture Assistant
Lecture API
=========================================================

Wrapper for Lecture Endpoints
"""

import logging

from api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class LectureAPI(BaseAPIClient):

    def __init__(self):

        super().__init__()

    # =====================================================
    # List Lectures
    # =====================================================

    def list_lectures(self):

        logger.info("=" * 70)
        logger.info("Fetching Lectures...")
        logger.info("=" * 70)

        response = self.get(

            "/metadata/lectures"

        )

        logger.info(

            f"Total Lectures : {len(response.get('data', []))}"

        )

        return response

    # =====================================================
    # Get Lecture Metadata
    # =====================================================

    def get_metadata(

        self,

        lecture_id

    ):

        logger.info(

            f"Fetching Metadata : {lecture_id}"

        )

        return self.get(

            f"/metadata/{lecture_id}"

        )

    # =====================================================
    # Delete Lecture
    # =====================================================

    def delete_lecture(

        self,

        lecture_id

    ):

        logger.info(

            f"Deleting Lecture : {lecture_id}"

        )

        return self.delete(

            f"/metadata/{lecture_id}"

        )