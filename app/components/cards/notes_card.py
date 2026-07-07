"""
=========================================================
AI Lecture Assistant
Notes Card
Production Version
=========================================================

Responsibilities
----------------
1. Generate Notes
2. Display Notes
3. Download Notes
4. Regenerate Notes
"""

import logging

import streamlit as st

from api.notes_api import NotesAPI
from components.cards.base_card import BaseCard
from state.session_manager import SessionManager

logger = logging.getLogger(__name__)


class NotesCard:

    def __init__(self):

        self.api = NotesAPI()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        BaseCard.start(

            "Lecture Notes",

            "📒"

        )

        lecture = SessionManager.get_lecture()

        if not lecture["lecture_id"]:

            BaseCard.warning(

                "Please select a lecture first."

            )

            BaseCard.end()

            return

        notes_type = st.selectbox(

            "Notes Type",

            [

                "detailed",

                "short",

                "bullet"

            ]

        )

        if st.button(

            "📒 Generate Notes",

            use_container_width=True

        ):

            self.generate_notes(

                lecture["lecture_id"],

                notes_type,

                use_cache=True

            )

        notes = SessionManager.get(

            "notes"

        )

        if notes:

            st.divider()

            st.subheader(

                "📒 Notes"

            )

            st.markdown(

                notes

            )

            # -----------------------------------------
            # Statistics
            # -----------------------------------------

            words = len(

                notes.split()

            )

            reading_time = max(

                1,

                round(words / 200)

            )

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
            # Download
            # -----------------------------------------

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.download_button(

                    "⬇ Download TXT",

                    data=notes,

                    file_name="lecture_notes.txt",

                    mime="text/plain",

                    use_container_width=True

                )

            with col2:

                st.download_button(

                    "⬇ Download Markdown",

                    data=notes,

                    file_name="lecture_notes.md",

                    mime="text/markdown",

                    use_container_width=True

                )

            # -----------------------------------------
            # Regenerate
            # -----------------------------------------

            if st.button(

                "🔄 Regenerate Notes",

                use_container_width=True,

                key="regenerate_notes"

            ):

                self.generate_notes(

                    lecture["lecture_id"],

                    notes_type,

                    use_cache=False

                )

        BaseCard.end()

    # =====================================================
    # Generate Notes
    # =====================================================

    def generate_notes(

        self,

        lecture_id,

        notes_type,

        use_cache=True

    ):

        try:

            with st.spinner(

                "Generating Notes..."

            ):

                response = self.api.generate(

                    lecture_id=lecture_id,

                    notes_type=notes_type,

                    use_cache=use_cache

                )

            notes = response["data"]["notes"]

            SessionManager.set(

                "notes",

                notes

            )

            logger.info(

                "Notes generated successfully."

            )

            st.success(

                "Notes generated successfully."

            )

            st.rerun()

        except Exception as e:

            logger.exception(e)

            st.error(

                str(e)

            )