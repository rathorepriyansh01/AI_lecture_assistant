"""
=========================================================
AI Lecture Assistant
Quiz Player
Production Version
=========================================================

Responsibilities
----------------
1. Display One Question
2. Save User Answer
3. Previous / Next Navigation
4. Progress Bar
"""

import streamlit as st

from state.session_manager import SessionManager


class QuizPlayer:

    # =====================================================
    # Render
    # =====================================================

    def render(self, quiz):

        if not quiz:

            return

        current = SessionManager.get(

            "current_question",

            0

        )

        total = len(quiz)

        question = quiz[current]

        # ---------------------------------------------
        # Progress
        # ---------------------------------------------

        st.progress(

            (current + 1) / total

        )

        st.caption(

            f"Question {current + 1} of {total}"

        )

        st.divider()

        # ---------------------------------------------
        # Question
        # ---------------------------------------------

        st.markdown(

            f"### {question['question']}"

        )

        answers = SessionManager.get(

            "quiz_answers",

            {}

        )

        previous_answer = answers.get(

            question["id"]

        )

        answer = st.radio(

            "Choose your answer",

            question["options"],

            index=(
                question["options"].index(previous_answer)
                if previous_answer in question["options"]
                else None
            ),

            key=f"question_{question['id']}"

        )

        answers[question["id"]] = answer

        SessionManager.set(

            "quiz_answers",

            answers

        )

        st.divider()

        # ---------------------------------------------
        # Navigation
        # ---------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if current > 0:

                if st.button(

                    "⬅ Previous",

                    use_container_width=True

                ):

                    SessionManager.set(

                        "current_question",

                        current - 1

                    )

                    st.rerun()

        with col2:

            if current < total - 1:

                if st.button(

                    "Next ➡",

                    use_container_width=True

                ):

                    SessionManager.set(

                        "current_question",

                        current + 1

                    )

                    st.rerun()