"""
=========================================================
AI Lecture Assistant
Quiz Settings
Production Version
=========================================================

Responsibilities
----------------
1. Select Difficulty
2. Select Total Questions
3. Generate Quiz Button
"""

import streamlit as st


class QuizSettings:

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        st.subheader("⚙️ Quiz Settings")

        difficulty = st.selectbox(

            "Difficulty",

            [

                "easy",

                "medium",

                "hard"

            ],

            index=1

        )

        total_questions = st.slider(

            "Total Questions",

            min_value=5,

            max_value=30,

            value=10,

            step=5

        )

        generate = st.button(

            "🧠 Generate Quiz",

            use_container_width=True,

            type="primary"

        )

        return {

            "difficulty": difficulty,

            "total_questions": total_questions,

            "generate": generate

        }