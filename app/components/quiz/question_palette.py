"""
=========================================================
AI Lecture Assistant
Question Palette
Production Version
=========================================================

Responsibilities
----------------
1. Display Question Palette
2. Jump To Question
3. Show Answer Status
"""

import streamlit as st

from state.session_manager import SessionManager


class QuestionPalette:

    # =====================================================
    # Render
    # =====================================================

    def render(self, quiz):

        if not quiz:

            return

        st.divider()

        st.subheader("🗂 Question Palette")

        answers = SessionManager.get(

            "quiz_answers",

            {}

        )

        current = SessionManager.get(

            "current_question",

            0

        )

        columns = st.columns(5)

        for index, question in enumerate(quiz):

            # -----------------------------------------
            # Status Icon
            # -----------------------------------------

            if index == current:

                icon = "🟡"

            elif question["id"] in answers:

                icon = "🟢"

            else:

                icon = "⚪"

            with columns[index % 5]:

                if st.button(

                    f"{icon} {index + 1}",

                    key=f"palette_{index}",

                    use_container_width=True

                ):

                    SessionManager.set(

                        "current_question",

                        index

                    )

                    st.rerun()