from importlib import metadata
import json
import time
import logging
from pathlib import Path

from backend.core.llm import LLMManager
from backend.core.prompt_manager import PromptManager
from backend.generators import quiz
from backend.utils.metadata_manager import MetadataManager

logger = logging.getLogger(__name__)


class QuizService:

    def __init__(self):

        logger.info("=" * 70)
        logger.info("Initializing Quiz Service...")
        logger.info("=" * 70)

        self.llm = LLMManager()
        self.prompt_manager = PromptManager()
        self.manager = MetadataManager()

        self.supported_difficulty = [

            "easy",

            "medium",

            "hard"

        ]

        logger.info("Quiz Service Ready.")

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "service": "Quiz",

            "status": "healthy",

            "supported_difficulty": self.supported_difficulty,

            "cache": True

        }

    # =====================================================
    # Lecture Directory
    # =====================================================

    def get_lecture_directory(

        self,

        lecture_id

    ):

        return (

            Path(__file__).resolve().parents[2]

            / "data"

            / "lectures"

            / lecture_id

        )

    # =====================================================
    # Load Transcript
    # =====================================================

    def load_transcript(

        self,

        lecture_id

    ):

        lecture_dir = self.get_lecture_directory(

            lecture_id

        )

        transcript_path = lecture_dir / "transcript.json"

        with open(

            transcript_path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(

        self,

        transcript

    ):

        context = []

        chunks = transcript["chunks"]

        for chunk in chunks:

            context.append(

                chunk["text"]

            )

        return "\n\n".join(context)

    # =====================================================
    # Split Context
    # =====================================================

    def split_context(

        self,

        context,

        chunk_size=12000

    ):

        return [

            context[i:i+chunk_size]

            for i in range(

                0,

                len(context),

                chunk_size

            )

        ]
    # =====================================================
    # Generate Chunk Quiz
    # =====================================================

    def generate_chunk_quiz(

        self,

        context,

        difficulty,

        total_questions

    ):

        prompt = self.prompt_manager.get_prompt(

            "quiz_prompt"

        )

        prompt = prompt.format(

            context=context,

            difficulty=difficulty,

            total_questions=total_questions

        )

        logger.info("=" * 70)
        logger.info("Generating Quiz Chunk...")
        logger.info("=" * 70)

        return self.llm.invoke(prompt)
    
    # =====================================================
    # Merge Quiz
    # =====================================================

    def merge_quiz(

        self,

        quizzes,

        difficulty,

        total_questions

    ):

        prompt = f"""

    You are an expert educator.

    Merge the following quiz parts into one final quiz.

    Requirements:

    - Difficulty : {difficulty}

    - Total Questions : {total_questions}

    - Remove duplicate questions.

    - Keep numbering continuous.

    - Keep answers.

    - Keep explanations.

    Quiz Parts:

    {chr(10).join(quizzes)}

    Return ONLY markdown.

    """

        logger.info("=" * 70)
        logger.info("Merging Quiz...")
        logger.info("=" * 70)

        return self.llm.invoke(prompt)
    # =====================================================
    # Generate Quiz
    # =====================================================

    def generate(

    self,

    lecture_id,

    difficulty="medium",

    total_questions=20,

    use_cache=True

):

        difficulty = self.validate_input(

        difficulty,

        total_questions

    )

        if use_cache:

            quiz = self.load_quiz(

                lecture_id

            )

            if quiz is not None:

                logger.info(

                    "Quiz Loaded From Cache."

                )

                return {

                "quiz": quiz,

                "cached": True,

                "statistics": {}

                }

        start = time.time()

        logger.info("=" * 70)
        logger.info("Generating Quiz...")
        logger.info("=" * 70)

        transcript = self.load_transcript(

            lecture_id

        )

        context = self.build_context(

            transcript

        )

        parts = [context]

        quizzes = []

        questions_per_part = max(

            1,

            total_questions // len(parts)

        )

        for part in parts:

            quiz = self.generate_chunk_quiz(

                part,

                difficulty,

                questions_per_part

            )
            print("=" * 80)
            print("TYPE :", type(quiz))
            print("VALUE :", quiz)
            print("=" * 80)

            quizzes.append(

                quiz

            )

        final_quiz = quizzes[0]

        execution_time = round(

            time.time() - start,

            2

        )

        logger.info("=" * 70)
        logger.info("Quiz Generated Successfully")
        logger.info("=" * 70)

        quiz_json = {

        "lecture_id": lecture_id,

        "difficulty": difficulty,

        "questions": total_questions,

        "quiz": final_quiz

    }

        self.save_quiz(

        lecture_id,

        final_quiz,

        quiz_json

    )
        metadata = self.manager.load(

            lecture_id

        )

        metadata["features"]["quiz_generated"] = True

        metadata["exports"]["quiz_path"] = str(

            self.get_lecture_directory(

                lecture_id

            ) / "quiz.md"

        )

        self.manager.save(

            lecture_id,

            metadata

        )

        return {

            "cached": False,

            "quiz": final_quiz,

            "statistics": {

                "execution_time": execution_time,

                "parts": len(parts),

                "questions": total_questions

            }

        }
    # =====================================================
    # Validate Input
    # =====================================================

    def validate_input(

        self,

        difficulty,

        total_questions

    ):

        difficulty = difficulty.lower()

        if difficulty not in self.supported_difficulty:

            raise ValueError(

                f"""

    Invalid Difficulty

    Supported:

    easy

    medium

    hard

    """

            )

        if total_questions <= 0:

            raise ValueError(

                "Total Questions must be greater than 0."

            )

        return difficulty
    
    # =====================================================
    # Save Quiz
    # =====================================================

    def save_quiz(

        self,

        lecture_id,

        markdown,

        json_data

    ):

        lecture_dir = self.get_lecture_directory(

            lecture_id

        )

        markdown_path = lecture_dir / "quiz.md"

        json_path = lecture_dir / "quiz.json"

        with open(

            markdown_path,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(markdown)

        with open(

            json_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                json_data,

                f,

                indent=4,

                ensure_ascii=False

            )
        metadata = self.manager.load(

        lecture_id

        )
        metadata["features"]["quiz_generated"] = True

        metadata["exports"]["quiz_path"] = str(

            self.get_lecture_directory(

                    lecture_id

                ) / "quiz.md"

            )

        self.manager.save(

                lecture_id,

                metadata

)

        return markdown_path
    
    # =====================================================
    # Load Quiz
    # =====================================================

    def load_quiz(

        self,

        lecture_id

    ):

        lecture_dir = self.get_lecture_directory(

            lecture_id

        )

        markdown_path = lecture_dir / "quiz.md"

        if not markdown_path.exists():

            return None

        with open(

            markdown_path,

            "r",

            encoding="utf-8"

        ) as f:

            return f.read()