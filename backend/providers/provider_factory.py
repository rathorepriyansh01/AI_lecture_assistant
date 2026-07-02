"""
=========================================================
AI Lecture Assistant
Provider Factory
=========================================================
"""

import logging
import time

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from backend.providers.groq_provider import GroqProvider
from backend.providers.nvidia_provider import NvidiaProvider

logger = logging.getLogger(__name__)


class ProviderFactory:

    def __init__(self):

        self.providers = {

            "groq": GroqProvider(
                api_key=GROQ_API_KEY,
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            ),

            "nvidia": NvidiaProvider(
                api_key=NVIDIA_API_KEY,
                model=NVIDIA_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )

        }

    # =====================================================
    # Get Provider
    # =====================================================

    def get_provider(
        self,
        provider_name: str
    ):

        provider_name = provider_name.lower()

        if provider_name not in self.providers:

            raise ValueError(
                f"Unknown Provider : {provider_name}"
            )

        return self.providers[provider_name]

    # =====================================================
    # Safe Invoke
    # =====================================================

    def safe_invoke(

        self,

        prompt,

        primary="groq",

        retries=2

    ):

        providers_order = []

        primary = primary.lower()

        if primary == "groq":

            providers_order = [

                "groq",

                "nvidia"

            ]

        else:

            providers_order = [

                "nvidia",

                "groq"

            ]

        last_exception = None

        for provider_name in providers_order:

            provider = self.get_provider(

                provider_name

            )

            logger.info("=" * 70)
            logger.info(
                f"Trying Provider : {provider_name.upper()}"
            )
            logger.info("=" * 70)

            for attempt in range(retries):

                try:

                    response = provider.invoke(

                        prompt

                    )

                    logger.info(
                        f"Success : {provider_name.upper()}"
                    )

                    return {

                        "provider": provider_name,

                        "response": response

                    }

                except Exception as e:

                    last_exception = e

                    logger.warning(

                        f"{provider_name.upper()} "

                        f"Attempt {attempt+1}/{retries}"

                    )

                    logger.warning(str(e))

                    time.sleep(2)

            logger.warning(
                f"Switching Provider..."
            )
        result = self.safe_invoke(
            prompt,
            primary="groq"
        )   

        raise Exception(

            f"All Providers Failed.\n\n"

            f"Last Error:\n{last_exception}"

        )

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        status = {}

        for name, provider in self.providers.items():

            try:

                status[name] = provider.health_check()

            except Exception as e:

                status[name] = {

                    "status": "failed",

                    "error": str(e)

                }

        return status