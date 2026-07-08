"""
=========================================================
AI Lecture Assistant
Review Answers
Production Version
=========================================================

Responsibilities
----------------
1. Display User Answers
2. Display Correct Answers
3. Highlight Correct / Wrong
"""

import streamlit as st

from state.session_manager import SessionManager


class ReviewAnswers:

    # =====================================================
    # Render
    # =====================================================

    def render(self, quiz):

        if not quiz:

            return

        answers = SessionManager.get(

            "quiz_answers",

            {}

        )

        st.divider()

        st.subheader("📖 Review Answers")

        for question in quiz:

            st.markdown("---")

            st.markdown(

                f"### Q{question['id']}. {question['question']}"

            )

            user_answer = answers.get(

                question["id"]

            )

            correct_index = question["labels"].index(

                question["correct_answer"]

            )

            correct_answer = question["options"][

                correct_index

            ]

            if user_answer == correct_answer:

                st.success(

                    f"✅ Your Answer : {user_answer}"

                )

            else:

                st.error(

                    f"❌ Your Answer : {user_answer}"

                )

                st.success(

                    f"✅ Correct Answer : {correct_answer}"

                )

            # Future Support
            if "explanation" in question:

                st.info(

                    question["explanation"]

                )