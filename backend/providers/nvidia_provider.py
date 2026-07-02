"""
=========================================================
NVIDIA Provider
=========================================================
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
        logger.info("Initializing NVIDIA Provider...")
        logger.info("=" * 70)

        self.client = ChatNVIDIA(

            api_key=self.api_key,

            model=self.model,

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

    ):

        response = self.client.invoke(

            prompt

        )

        return response.content
    
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