"""
=========================================================
AI Lecture Assistant
Chatbot Service
Production Version
=========================================================
"""

import logging
import time

from backend.services.retrieval_service import RetrieverService
from backend.core.prompt_manager import PromptManager
from backend.core.llm import LLMManager

# ==========================================================
# LOGGER
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# Chatbot Service
# ==========================================================

class ChatbotService:

    def __init__(self):

        logger.info("=" * 70)
        logger.info("Initializing Chatbot Service...")
        logger.info("=" * 70)

        # --------------------------------------------
        # Shared Components
        # --------------------------------------------

        self.retriever = RetrieverService()

        self.prompt_manager = PromptManager()

        self.llm = LLMManager()

        logger.info("Retriever Loaded")

        logger.info("Prompt Manager Loaded")

        logger.info("LLM Loaded")

        logger.info("=" * 70)

        # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "retriever": self.retriever.health_check(),

            "llm": self.llm.health_check(),

            "prompts": self.prompt_manager.available_prompts()

        }
    # =====================================================
    # Retrieve Context
    # =====================================================

    def retrieve_context(
        self,
        question: str,
        lecture_id: str = None
    ):

        logger.info("=" * 70)
        logger.info("Retrieving Lecture Context...")
        logger.info("=" * 70)

        start = time.time()

        retrieval = self.retriever.retrieve(

            question=question,

            lecture_id=lecture_id

        )

        elapsed = round(

            time.time() - start,

            3

        )

        logger.info(

            f"Retrieved {retrieval['count']} chunks."

        )

        logger.info(

            f"Context Length : {len(retrieval['context'])}"

        )

        logger.info(

            f"Retrieval Time : {elapsed} sec"

        )

        logger.info("=" * 70)

        return retrieval
    # =====================================================
    # Build Prompt
    # =====================================================

    def build_prompt(
        self,
        question: str,
        context: str
    ):

        logger.info("=" * 70)
        logger.info("Formatting Prompt...")
        logger.info("=" * 70)

        prompt = self.prompt_manager.format_prompt(

            "chatbot",

            context=context,

            question=question

        )

        logger.info(

            f"Prompt Length : {len(prompt)}"

        )

        logger.info("=" * 70)

        return prompt
    # =====================================================
    # Generate Answer
    # =====================================================

    def generate_answer(
        self,
        prompt: str
    ):

        logger.info("=" * 70)
        logger.info("Generating Answer...")
        logger.info("=" * 70)

        start = time.time()

        answer = self.llm.invoke(
            prompt
        )

        elapsed = round(
            time.time() - start,
            3
        )

        logger.info(
            f"Generation Time : {elapsed} sec"
        )

        logger.info("=" * 70)

        return answer, elapsed
    # =====================================================
    # Format Response
    # =====================================================

    def format_response(
        self,
        answer: str
    ):

        logger.info("Formatting Response...")

        if answer is None:
            return ""

        answer = answer.strip()

        # Remove extra blank lines
        while "\n\n\n" in answer:

            answer = answer.replace(
                "\n\n\n",
                "\n\n"
            )

        return answer
    # =====================================================
    # Ask
    # =====================================================

    def ask(
        self,
        question: str,
        lecture_id: str = None
    ):

        logger.info("=" * 70)
        logger.info("Chatbot Pipeline Started")
        logger.info("=" * 70)

        overall_start = time.time()

        try:

            # ------------------------------------------
            # Retrieve Context
            # ------------------------------------------

            retrieval = self.retrieve_context(
                question=question,
                lecture_id=lecture_id
            )

            retrieval_time = retrieval["statistics"].get(
                "execution_time",
                0
            )

            # ------------------------------------------
            # Build Prompt
            # ------------------------------------------

            prompt = self.build_prompt(
                question=question,
                context=retrieval["context"]
            )

            # ------------------------------------------
            # Generate Answer
            # ------------------------------------------

            answer, generation_time = self.generate_answer(
                prompt
            )

            # ------------------------------------------
            # Clean Answer
            # ------------------------------------------

            answer = self.format_response(
                answer
            )

            total_time = round(
                time.time() - overall_start,
                3
            )

            logger.info("=" * 70)
            logger.info("Chatbot Finished")
            logger.info(f"Total Time : {total_time} sec")
            logger.info("=" * 70)

            return {

                "question": question,

                "answer": answer,

                "sources": retrieval["sources"],

                "context_length": len(
                    retrieval["context"]
                ),

                "statistics": {

                    "retrieval_time": retrieval_time,

                    "generation_time": generation_time,

                    "total_time": total_time

                }

            }

        except Exception as e:

            logger.exception(
                "Chatbot Failed"
            )

            raise e