"""
=========================================================
AI Lecture Assistant
LLM Manager
=========================================================

STATUS : FINAL
Version : 1.0
"""

import logging

from config.settings import (
    LLM_PROVIDER,
    PRIMARY_PROVIDER
)

from backend.providers.provider_factory import (
    ProviderFactory
)

logger = logging.getLogger(__name__)


class LLMManager:
    """
    Singleton LLM Manager

    Acts as a single entry point for all
    AI Services.

    Summary
    Notes
    Quiz
    Flashcards
    Mindmap

    should always call

        self.llm.invoke(...)
    """

    _instance = None
    _factory = None

    # =====================================================
    # Singleton
    # =====================================================

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        if LLMManager._factory is not None:

            return

        logger.info("=" * 70)
        logger.info("Initializing LLM Manager...")
        logger.info("=" * 70)

        self.default_provider = (

            LLM_PROVIDER

            or

            PRIMARY_PROVIDER

        ).lower()

        LLMManager._factory = ProviderFactory()

        logger.info(

            f"Default Provider : "

            f"{self.default_provider.upper()}"

        )

        logger.info("=" * 70)

    # =====================================================
    # Factory
    # =====================================================

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

    ) -> str:

        provider = (

            provider

            or

            self.default_provider

        )

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

    # =====================================================
    # Statistics
    # =====================================================

    def get_statistics(self):

        return self.factory.get_statistics()

    # =====================================================
    # Reset Provider
    # =====================================================

    def reset_provider(

        self,

        provider

    ):

        self.factory.reset_provider(

            provider

        )

    # =====================================================
    # Clear Statistics
    # =====================================================

    def clear_statistics(self):

        self.factory.clear_statistics()

    # =====================================================
    # Change Default Provider
    # =====================================================

    def set_default_provider(

        self,

        provider

    ):

        provider = provider.lower()

        if provider not in [

            "gemini",

            "groq",

            "nvidia"

        ]:

            raise ValueError(

                f"Unknown Provider : {provider}"

            )

        self.default_provider = provider

        logger.info(

            f"Default Provider changed to "

            f"{provider.upper()}"

        )

    # =====================================================
    # Current Provider
    # =====================================================

    def get_default_provider(self):

        return self.default_provider

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return (

            "LLMManager("

            f"default_provider='{self.default_provider}')"

        )