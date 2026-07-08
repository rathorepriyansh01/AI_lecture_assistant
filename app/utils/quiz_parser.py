"""
=========================================================
AI Lecture Assistant
Quiz Parser
Production Version
=========================================================

Responsibilities
----------------
1. Parse Markdown Quiz
2. Extract Questions
3. Extract Options
4. Extract Answer Key
"""

import re


class QuizParser:

    # =====================================================
    # Parse Quiz
    # =====================================================

    @staticmethod
    def parse(markdown: str):

        questions = []

        answer_key = {}

        # ---------------------------------------------
        # Split Answer Key
        # ---------------------------------------------

        if "**Answer Key:**" in markdown:

            quiz_text, answer_text = markdown.split(

                "**Answer Key:**",

                1

            )

        else:

            quiz_text = markdown

            answer_text = ""

        # ---------------------------------------------
        # Parse Answer Key
        # ---------------------------------------------

        answer_pattern = re.compile(

            r"(\d+)\.\s+\*\*([a-dA-D])\)"

        )

        for match in answer_pattern.finditer(answer_text):

            answer_key[int(match.group(1))] = (

                match.group(2).lower()

            )

        # ---------------------------------------------
        # Parse Questions
        # ---------------------------------------------

        question_pattern = re.compile(

            r"\*\*(\d+)\.\s*(.*?)\*\*(.*?)"
            r"(?=\n\*\*\d+\.|\Z)",

            re.S

        )

        option_pattern = re.compile(

            r"([a-d])\)\s+(.*)"

        )

        for match in question_pattern.finditer(quiz_text):

            question_id = int(

                match.group(1)

            )

            question = match.group(2).strip()

            body = match.group(3)

            options = []

            labels = []

            for opt in option_pattern.finditer(body):

                labels.append(

                    opt.group(1)

                )

                options.append(

                    opt.group(2).strip()

                )

            questions.append(

                {

                    "id": question_id,

                    "question": question,

                    "labels": labels,

                    "options": options,

                    "correct_answer": answer_key.get(

                        question_id

                    )

                }

            )

        return questions