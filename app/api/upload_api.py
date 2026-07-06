"""
=========================================================
AI Lecture Assistant
Upload API
=========================================================

Wrapper for Upload Endpoints
"""

import logging
from pathlib import Path

from app.api.base_client import BaseAPIClient

logger = logging.getLogger(__name__)


class UploadAPI(BaseAPIClient):

    def __init__(self):

        super().__init__()

    # =====================================================
    # Upload Video
    # =====================================================

    def upload_video(
        self,
        video_path
    ):

        video_path = Path(video_path)

        if not video_path.exists():

            raise FileNotFoundError(

                f"Video not found : {video_path}"

            )

        logger.info("=" * 70)
        logger.info("Uploading Lecture...")
        logger.info("=" * 70)

        with open(video_path, "rb") as file:

            files = {

                "file": (

                    video_path.name,

                    file,

                    "video/mp4"

                )

            }

            response = self.post(

                "/upload",

                files=files

            )

        logger.info("Upload Completed.")

        return response