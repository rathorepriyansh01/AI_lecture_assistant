"""
=========================================================
AI Lecture Assistant
Gemini Provider
=========================================================
STATUS : FINAL
Version : 1.0
"""

import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from backend.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseProvider):

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
        logger.info("Initializing Gemini Provider...")
        logger.info("=" * 70)

        self.client = ChatGoogleGenerativeAI(

            model=self.model,

            google_api_key=self.api_key,

            temperature=self.temperature,

            max_output_tokens=self.max_tokens

        )

        logger.info("Gemini Provider Ready.")

    # =====================================================
    # Normalize Response
    # =====================================================

    def _normalize_response(
        self,
        content
    ) -> str:

        if content is None:
            return ""

        # Already string
        if isinstance(content, str):
            return content.strip()

        # List returned by Gemini
        if isinstance(content, list):

            output = []

            for item in content:

                if hasattr(item, "text"):

                    output.append(
                        item.text
                    )

                elif isinstance(item, dict):

                    output.append(
                        item.get("text", "")
                    )

                else:

                    output.append(
                        str(item)
                    )

            return "\n".join(output).strip()

        # Object with text attribute
        if hasattr(content, "text"):

            return str(
                content.text
            ).strip()

        return str(content).strip()

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

            return self._normalize_response(
                response.content
            )

        except Exception as e:

            logger.exception(
                "Gemini Invocation Failed"
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

            "provider": "Gemini",

            "model": self.model,

            "temperature": self.temperature,

            "max_tokens": self.max_tokens

        }

    # =====================================================
    # Provider Info
    # =====================================================

    def __repr__(self):

        return (

            f"GeminiProvider("

            f"model='{self.model}', "

            f"temperature={self.temperature})"

        )