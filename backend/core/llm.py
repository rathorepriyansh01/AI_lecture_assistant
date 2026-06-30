"""
=========================================================
AI Lecture Assistant
Shared LLM Manager
Production Version
=========================================================

Supports:
- Groq
- Gemini (Future)
"""

import logging
from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class LLMManager:

    _instance = None
    _llm = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if LLMManager._llm is None:

            self.provider = "Groq"

            self.model_name = GROQ_MODEL

            self.temperature = TEMPERATURE

            self.max_tokens = MAX_TOKENS

            logger.info("=" * 70)
            logger.info("Loading Groq LLM...")
            logger.info("=" * 70)

            LLMManager._llm = ChatGroq(

                api_key=GROQ_API_KEY,

                model=self.model_name,

                temperature=self.temperature,

                max_tokens=self.max_tokens

    )

    @property
    def llm(self):
        return LLMManager._llm

    # ======================================================
    # Ask LLM
    # ======================================================

    def invoke(
        self,
        prompt: str
    ):

        response = self.llm.invoke(prompt)

        return response.content
    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

        "status": "healthy",

        "provider": self.provider,

        "model": self.model_name,

        "temperature": self.temperature,

        "max_tokens": self.max_tokens

    }
    # ======================================================
    # Chat
    # ======================================================

    def chat(
        self,
        system_prompt,
        user_prompt
    ):

        prompt = f"""

{system_prompt}

-----------------------------------

{user_prompt}

"""

        response = self.llm.invoke(prompt)

        return response.content