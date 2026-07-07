"""
=========================================================
AI Lecture Assistant
Lecture Selector Component
=========================================================

Responsibilities
----------------
1. Display Available Lectures
2. Select Current Lecture
3. Update Session
"""

import logging
import streamlit as st

from api.lecture_api import LectureAPI
from state.session_manager import SessionManager

logger = logging.getLogger(__name__)


class LectureSelector:

    def __init__(self):

        self.api = LectureAPI()

    

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        response = self.api.list_lectures()

        lectures = response.get("data", [])

        if not lectures:

            st.info(
                "No lectures available. Please upload a lecture."
            )
            return None

        lecture_names = [
            lecture["lecture_name"]
            for lecture in lectures
        ]

        current = SessionManager.get("lecture_name")

        index = 0

        if current in lecture_names:

            index = lecture_names.index(current)

        selected_name = st.selectbox(
            "Select Lecture",
            lecture_names,
            index=index
        )

        selected = next(
            (
                lecture
                for lecture in lectures
                if lecture["lecture_name"] == selected_name
            ),
            None
        )

        if selected is None:

            st.error("Lecture not found.")

            return None

        SessionManager.set_lecture(
            selected["lecture_id"],
            selected["lecture_name"]
        )

        metadata = self.api.get_metadata(
            selected["lecture_id"]
        )

        SessionManager.set(
            "metadata",
            metadata["data"]
        )

        logger.info(
            f"Lecture Selected : {selected_name}"
        )

        return metadata["data"]