"""
=========================================================
AI Lecture Assistant
NVIDIA Provider
=========================================================

STATUS : FINAL
Version : 1.0
Future Changes : NO
"""

import logging

from langchain_nvidia_ai_endpoints import ChatNVIDIA

from backend.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class NvidiaProvider(BaseProvider):

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
        logger.info("Initializing NVIDIA Provider...")
        logger.info("=" * 70)

        self.client = ChatNVIDIA(

            model=self.model,

            api_key=self.api_key,

            temperature=self.temperature,

            max_tokens=self.max_tokens

        )

        logger.info("NVIDIA Provider Ready.")

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
                    "Empty response received from NVIDIA."
                )

            if hasattr(response, "content"):

                content = response.content

                if isinstance(content, str):

                    return content.strip()

                return str(content).strip()

            return str(response).strip()

        except Exception as e:

            logger.exception(
                "NVIDIA Invocation Failed"
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

            "provider": "NVIDIA",

            "model": self.model,

            "temperature": self.temperature,

            "max_tokens": self.max_tokens

        }

    # =====================================================
    # Provider Info
    # =====================================================

    def __repr__(self):

        return (

            f"NvidiaProvider("

            f"model='{self.model}', "

            f"temperature={self.temperature})"

        )