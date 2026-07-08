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

    @staticmethod
    def parse(markdown: str):

        if not markdown:

            return []

        questions = []
        answer_key = {}

        # --------------------------------------------------
        # Split Quiz and Answer Key
        # --------------------------------------------------

        if "**Answer Key:**" in markdown:

            quiz_text, answer_text = markdown.split(
                "**Answer Key:**",
                1
            )

        else:

            quiz_text = markdown
            answer_text = ""

        # --------------------------------------------------
        # Parse Answer Key
        # --------------------------------------------------

        for line in answer_text.splitlines():

            line = line.strip()

            match = re.match(

                r"(\d+)\.\s*\*\*([a-dA-D])\)",

                line

            )

            if match:

                answer_key[int(match.group(1))] = (

                    match.group(2).lower()

                )

        # --------------------------------------------------
        # Parse Questions
        # --------------------------------------------------

        current = None

        for raw in quiz_text.splitlines():

            line = raw.strip()

            if not line:

                continue

            # ------------------------------------------
            # Skip headings
            # ------------------------------------------

            if line.startswith("---"):

                continue

            if line.lower().startswith("here are"):

                continue

            if "Multiple Choice Questions" in line:

                continue

            # ------------------------------------------
            # Question
            # ------------------------------------------

            q = re.match(

                r"\*\*(\d+)\.\s*(.*?)\*\*$",

                line

            )

            if q:

                if current:

                    questions.append(current)

                current = {

                    "id": int(q.group(1)),

                    "question": q.group(2).strip(),

                    "options": [],

                    "labels": [],

                    "correct_answer": None

                }

                continue

            # ------------------------------------------
            # Option
            # ------------------------------------------

            o = re.match(

                r"([a-dA-D])\)\s+(.*)",

                line

            )

            if o and current:

                current["labels"].append(

                    o.group(1).lower()

                )

                current["options"].append(

                    o.group(2).strip()

                )

        if current:

            questions.append(current)

        # --------------------------------------------------
        # Attach Answer Key
        # --------------------------------------------------

        for q in questions:

            q["correct_answer"] = answer_key.get(

                q["id"]

            )

        return questions