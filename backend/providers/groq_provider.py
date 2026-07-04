"""
=========================================================
AI Lecture Assistant
Groq Provider
=========================================================

STATUS : FINAL
Version : 1.0
Future Changes : NO
"""

import logging

from langchain_groq import ChatGroq

from backend.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class GroqProvider(BaseProvider):

    def __init__(
        self,
        api_key,
        model,
        temperature,
        max_tokens
    ):

        super().__init__(
            api_key,
            model,
            temperature,
            max_tokens
        )

        logger.info("=" * 70)
        logger.info("Initializing Groq Provider...")
        logger.info("=" * 70)

        self.client = ChatGroq(

            api_key=self.api_key,

            model=self.model,

            temperature=self.temperature,

            max_tokens=self.max_tokens

        )

        logger.info("Groq Provider Ready.")

    # =====================================================
    # Invoke
    # =====================================================

    def invoke(
        self,
        prompt
    ) -> str:

        try:

            response = self.client.invoke(
                prompt
            )

            if response is None:

                raise RuntimeError(
                    "Empty response received from Groq."
                )

            if hasattr(response, "content"):

                return str(
                    response.content
                ).strip()

            return str(
                response
            ).strip()

        except Exception as e:

            logger.exception(
                "Groq Invocation Failed"
            )

            raise RuntimeError(
                str(e)
            )

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "status": "healthy",

            "provider": "Groq",

            "model": self.model,

            "temperature": self.temperature,

            "max_tokens": self.max_tokens

        }

    # =====================================================
    # Provider Info
    # =====================================================

    def __repr__(self):

        return (

            f"GroqProvider("

            f"model='{self.model}', "

            f"temperature={self.temperature})"

        )