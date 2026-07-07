"""
=========================================================
AI Lecture Assistant
Summary Card
Production Version
=========================================================

Responsibilities
----------------
1. Generate Summary
2. Display Summary
3. Handle Loading State
"""

import logging

import streamlit as st

from api.summary_api import SummaryAPI
from components.cards.base_card import BaseCard
from state.session_manager import SessionManager

logger = logging.getLogger(__name__)


class SummaryCard:

    def __init__(self):

        self.api = SummaryAPI()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        BaseCard.start(

            "Lecture Summary",

            "📝"

        )

        lecture = SessionManager.get_lecture()

        if not lecture["lecture_id"]:

            BaseCard.warning(

                "Please select a lecture first."

            )

            BaseCard.end()

            return

        if st.button(

            "📝 Generate Summary",

            use_container_width=True

        ):

            self.generate_summary(

                lecture["lecture_id"]

            )

        summary = SessionManager.get("summary")

        if summary:

            st.divider()

            st.subheader("📝 Summary")

            st.markdown(summary)

            # -----------------------------------------
            # Statistics
            # -----------------------------------------

            words = len(summary.split())

            reading_time = max(1, round(words / 200))

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Words",

                    words

                )

            with col2:

                st.metric(

                    "Reading Time",

                    f"{reading_time} min"

                )

            # -----------------------------------------
            # Downloads
            # -----------------------------------------

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(

                    label="⬇ Download TXT",

                    data=summary,

                    file_name="lecture_summary.txt",

                    mime="text/plain",

                    use_container_width=True

                )

            with col2:

                st.download_button(

                    label="⬇ Download Markdown",

                    data=summary,

                    file_name="lecture_summary.md",

                    mime="text/markdown",

                    use_container_width=True

                )

            # -----------------------------------------
            # Regenerate
            # -----------------------------------------

            if st.button(

                "🔄 Regenerate Summary",

                use_container_width=True

            ):

                self.generate_summary(

                    lecture["lecture_id"]

                )

    # =====================================================
    # Generate Summary
    # =====================================================

    def generate_summary(
    self,
    lecture_id
):

        try:

            with st.spinner(
                "Generating summary..."
            ):

                response = self.api.generate(
                    lecture_id
                )

            # -----------------------------------------
            # Extract Summary
            # -----------------------------------------

            summary = response["data"]["summary"]

            SessionManager.set(
                "summary",
                summary
            )

            logger.info(
                "Summary generated successfully."
            )

            st.success(
                "Summary generated successfully."
            )

            st.rerun()

        except Exception as e:

            logger.exception(e)

            st.error(str(e))