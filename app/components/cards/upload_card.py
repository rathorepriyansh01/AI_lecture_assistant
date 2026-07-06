"""
=========================================================
AI Lecture Assistant
Upload Card
Production Version
=========================================================

Responsibilities
----------------
1. Select Video
2. Upload Video
3. Return Upload Response
"""

import logging
from pathlib import Path

import streamlit as st

from api.upload_api import UploadAPI
from components.cards.base_card import BaseCard

logger = logging.getLogger(__name__)


class UploadCard:

    def __init__(self):

        self.api = UploadAPI()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        BaseCard.start(

            "Upload Lecture",

            "📤"

        )

        uploaded_file = st.file_uploader(

            label="Choose Lecture Video",

            type=[

                "mp4",

                "avi",

                "mov",

                "mkv"

            ],

            accept_multiple_files=False

        )

        if uploaded_file is None:

            BaseCard.info(

                "Please choose a lecture video."

            )

            BaseCard.end()

            return None

        st.write(f"**Selected File:** {uploaded_file.name}")

        if not st.button(

            "🚀 Upload Lecture",

            use_container_width=True

        ):

            BaseCard.end()

            return None

        temp_path = Path("temp") / uploaded_file.name

        temp_path.parent.mkdir(

            exist_ok=True

        )

        with open(

            temp_path,

            "wb"

        ) as f:

            f.write(

                uploaded_file.getbuffer()

            )

        try:

            with st.spinner(

                "Uploading lecture..."

            ):

                response = self.api.upload_video(

                    temp_path

                )

            logger.info(

                "Lecture uploaded successfully."

            )

            return response

        finally:

            if temp_path.exists():

                temp_path.unlink()

            BaseCard.end()