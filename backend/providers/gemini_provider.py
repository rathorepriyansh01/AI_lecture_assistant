"""
=========================================================
AI Lecture Assistant
Gemini Provider
=========================================================
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

        temperature=0.2,

        max_tokens=2048

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

            google_api_key=self.api_key,

            model=self.model,

            temperature=self.temperature,

            max_output_tokens=self.max_tokens

        )

        logger.info("Gemini Provider Ready.")

    # =====================================================
    # Invoke
    # =====================================================

    def invoke(

        self,

        prompt: str

    ):

        response = self.client.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):

            output = []

            for part in content:

                if hasattr(part, "text"):
                    output.append(part.text)

                elif isinstance(part, dict):
                    output.append(part.get("text", ""))

                else:
                    output.append(str(part))

            return "\n".join(output)

        return str(content)

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
    # Provider Name
    # =====================================================

    @property
    def provider_name(self):

        return "gemini"