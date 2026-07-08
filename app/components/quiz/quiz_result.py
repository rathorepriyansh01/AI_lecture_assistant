"""
=========================================================
AI Lecture Assistant
Quiz Result
Production Version
=========================================================

Responsibilities
----------------
1. Display Quiz Score
2. Display Statistics
3. Retry Quiz
"""

import streamlit as st

from state.session_manager import SessionManager


class QuizResult:

    # =====================================================
    # Render
    # =====================================================

    def render(

        self,

        score,

        total_questions,

        time_taken=None

    ):

        st.divider()

        st.subheader("🎉 Quiz Completed")

        accuracy = 0

        if total_questions > 0:

            accuracy = round(

                score / total_questions * 100,

                2

            )

        correct = score

        wrong = total_questions - score

        # -----------------------------------------
        # Metrics
        # -----------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Score",

                f"{score}/{total_questions}"

            )

        with col2:

            st.metric(

                "Accuracy",

                f"{accuracy}%"

            )

        with col3:

            st.metric(

                "Correct",

                correct

            )

        with col4:

            st.metric(

                "Wrong",

                wrong

            )

        if time_taken is not None:

            st.info(

                f"⏱ Time Taken : {time_taken}"

            )

        st.divider()

        # -----------------------------------------
        # Retry
        # -----------------------------------------

        if st.button(

            "🔄 Retry Quiz",

            use_container_width=True,

            type="primary"

        ):

            SessionManager.set(

                "quiz_answers",

                {}

            )

            SessionManager.set(

                "current_question",

                0

            )

            SessionManager.set(

                "quiz_score",

                0

            )

            SessionManager.set(

                "quiz_submitted",

                False

            )

            st.rerun()