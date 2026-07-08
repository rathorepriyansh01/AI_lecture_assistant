from api.quiz_api import QuizAPI

from components.cards.base_card import BaseCard

from components.quiz.quiz_settings import QuizSettings
from components.quiz.quiz_player import QuizPlayer
from components.quiz.question_palette import QuestionPalette
from components.quiz.quiz_result import QuizResult
from components.quiz.review_answers import ReviewAnswers

from state.session_manager import SessionManager
from utils.quiz_parser import QuizParser

import streamlit as st
import logging

class QuizCard:

    def __init__(self):

        self.api = QuizAPI()

        self.settings = QuizSettings()

        self.player = QuizPlayer()

        self.palette = QuestionPalette()

        self.result = QuizResult()

        self.review = ReviewAnswers()

    def calculate_score(self, quiz):

        answers = SessionManager.get(

            "quiz_answers",

            {}

        )

        score = 0

        for question in quiz:

            user_answer = answers.get(

                question["id"]

            )

            if not user_answer:

                continue

            correct = question["options"][

                question["labels"].index(

                    question["correct_answer"]

                )

            ]

            if user_answer == correct:

                score += 1

        return score
    
    def render(self):

        BaseCard.start(

            "Lecture Quiz",

            "🧠"

        )

        lecture = SessionManager.get_lecture()

        if not lecture["lecture_id"]:

            BaseCard.warning(

                "Please select a lecture."

            )

            BaseCard.end()

            return

        settings = self.settings.render()

        if settings["generate"]:

            self.generate_quiz(

                lecture["lecture_id"],

                settings["difficulty"],

                settings["total_questions"]

            )

        quiz = SessionManager.get(

            "quiz"

        )

        if not quiz:

            BaseCard.end()

            return

        self.player.render(

            quiz

        )

        self.palette.render(

            quiz

        )

        st.divider()

        if st.button(

            "✅ Submit Quiz",

            type="primary",

            use_container_width=True

        ):

            SessionManager.set(

                "quiz_submitted",

                True

            )

            st.rerun()

        if SessionManager.get(

            "quiz_submitted"

        ):

            score = self.calculate_score(

                quiz

            )

            SessionManager.set(

                "quiz_score",

                score

            )

            self.result.render(

                score,

                len(quiz)

            )

            self.review.render(

                quiz

            )

        BaseCard.end()

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
            use_cache=True
        )

            st.subheader("API Response")
            st.json(response)

            quiz = QuizParser.parse(response["data"]["quiz"])

            st.write(type(quiz))
            st.write(len(quiz))
            st.write(quiz)

            st.subheader("Parsed Quiz")
            st.write(quiz)

            SessionManager.set("quiz", quiz)

            st.subheader("Quiz in Session")
            st.write(SessionManager.get("quiz"))

            quiz = QuizParser.parse(

            response["data"]["quiz"]

            )

            SessionManager.set(

                "quiz",

                quiz

            )

            SessionManager.set(

                "quiz_answers",

                {}

            )

            SessionManager.set(

                "current_question",

                0

            )

            SessionManager.set(

                "quiz_submitted",

                False

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