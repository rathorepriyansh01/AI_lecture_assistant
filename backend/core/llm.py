"""
=========================================================
AI Lecture Assistant
LLM Manager
=========================================================
"""

import logging

from config.settings import LLM_PROVIDER
from backend.providers.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


class LLMManager:

    _instance = None
    _factory = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if LLMManager._factory is None:

            logger.info("=" * 70)
            logger.info("Initializing LLM Manager...")
            logger.info("=" * 70)

            self.default_provider = LLM_PROVIDER.lower()

            LLMManager._factory = ProviderFactory()

            logger.info(
                f"Default Provider : {self.default_provider.upper()}"
            )

            logger.info("=" * 70)

    @property
    def factory(self):

        return LLMManager._factory

    # =====================================================
    # Invoke
    # =====================================================

    def invoke(

        self,

        prompt,

        provider=None

    ):

        provider = provider or self.default_provider

        result = self.factory.safe_invoke(

            prompt,

            primary=provider

        )

        return result["response"]

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return self.factory.health_check()