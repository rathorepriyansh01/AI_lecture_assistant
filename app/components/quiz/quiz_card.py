"""
=========================================================
AI Lecture Assistant
Quiz Card
Production Version
=========================================================

Responsibilities
----------------
1. Generate Quiz
2. Parse Quiz
3. Display Interactive Quiz
4. Calculate Score
"""

import logging

import streamlit as st

from api.quiz_api import QuizAPI
from components.cards.base_card import BaseCard
from state.session_manager import SessionManager
from utils.quiz_parser import QuizParser

logger = logging.getLogger(__name__)


class QuizCard:

    def __init__(self):

        self.api = QuizAPI()

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        BaseCard.start(

            "Lecture Quiz",

            "🧠"

        )

        lecture = SessionManager.get_lecture()

        if not lecture["lecture_id"]:

            BaseCard.warning(

                "Please select a lecture first."

            )

            BaseCard.end()

            return

        difficulty = st.selectbox(

            "Difficulty",

            [

                "easy",

                "medium",

                "hard"

            ]

        )

        total_questions = st.slider(

            "Total Questions",

            min_value=5,

            max_value=30,

            value=10,

            step=5

        )

        if st.button(

            "🧠 Generate Quiz",

            use_container_width=True

        ):

            self.generate_quiz(

                lecture["lecture_id"],

                difficulty,

                total_questions

            )

        quiz = SessionManager.get(

            "quiz"

        )

        if quiz:

            self.render_quiz(

                quiz

            )

        BaseCard.end()

    # =====================================================
    # Generate Quiz
    # =====================================================

    def generate_quiz(

        self,

        lecture_id,

        difficulty,

        total_questions

    ):

        try:

            with st.spinner(

                "Generating Quiz..."

            ):

                response = self.api.generate(

                    lecture_id=lecture_id,

                    difficulty=difficulty,

                    total_questions=total_questions,

                    use_cache=False

                )

            quiz_markdown = response["data"]["quiz"]

            quiz = QuizParser.parse(

                quiz_markdown

            )

            SessionManager.set(

                "quiz",

                quiz

            )

            st.success(

                "Quiz generated successfully."

            )

            st.rerun()

        except Exception as e:

            logger.exception(e)

            st.error(

                str(e)

            )

    # =====================================================
    # Quiz Player
    # =====================================================

    def render_quiz(

        self,

        quiz

    ):

        st.divider()

        st.subheader(

            "📝 Quiz"

        )

        score = 0

        submitted = st.button(

            "Submit Quiz",

            use_container_width=True

        )

        for question in quiz:

            answer = st.radio(

                question["question"],

                question["options"],

                key=f"q_{question['id']}"

            )

            if submitted:

                index = question["labels"].index(

                    question["correct_answer"]

                )

                correct = question["options"][

                    index

                ]

                if answer == correct:

                    score += 1

        if submitted:

            st.divider()

            st.success(

                f"Score : {score} / {len(quiz)}"

            )

            percentage = round(

                score / len(quiz) * 100,

                2

            )

            st.metric(

                "Accuracy",

                f"{percentage}%"

            )