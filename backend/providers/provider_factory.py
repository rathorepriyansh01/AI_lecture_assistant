"""
=========================================================
AI Lecture Assistant
Provider Factory
=========================================================
"""

import logging
import time
from threading import Lock

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    PRIMARY_PROVIDER,
    SECONDARY_PROVIDER,
    THIRD_PROVIDER
)

from backend.providers.gemini_provider import GeminiProvider
from backend.providers.groq_provider import GroqProvider
from backend.providers.nvidia_provider import NvidiaProvider


logger = logging.getLogger(__name__)


class ProviderFactory:

    def __init__(self):

        self._lock = Lock()

        logger.info("=" * 70)
        logger.info("Initializing Provider Factory...")
        logger.info("=" * 70)

        # =====================================================
        # Register Providers
        # =====================================================

        self.providers = {

            "gemini": GeminiProvider(
                api_key=GEMINI_API_KEY,
                model=GEMINI_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            ),

            "groq": GroqProvider(
                api_key=GROQ_API_KEY,
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            ),

            "nvidia": NvidiaProvider(
                api_key=NVIDIA_API_KEY,
                model=NVIDIA_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )

        }

        # =====================================================
        # Provider Priority
        # =====================================================

        self.priority = [

            PRIMARY_PROVIDER.lower(),

            SECONDARY_PROVIDER.lower(),

            THIRD_PROVIDER.lower()

        ]

        # =====================================================
        # Health Cache
        # =====================================================

        self.health = {

            "gemini": {

                "available": True,

                "retry_after": 0

            },

            "groq": {

                "available": True,

                "retry_after": 0

            },

            "nvidia": {

                "available": True,

                "retry_after": 0

            }

        }

        # =====================================================
        # Statistics
        # =====================================================

        self.statistics = {

            "gemini": {

                "success": 0,

                "failure": 0,

                "retry": 0,

                "latency": []

            },

            "groq": {

                "success": 0,

                "failure": 0,

                "retry": 0,

                "latency": []

            },

            "nvidia": {

                "success": 0,

                "failure": 0,

                "retry": 0,

                "latency": []

            }

        }

        logger.info("Provider Factory Ready.")

    # =====================================================
    # Get Provider
    # =====================================================

    def get_provider(

        self,

        provider_name

    ):

        provider_name = provider_name.lower()

        if provider_name not in self.providers:

            raise ValueError(

                f"Unknown Provider : {provider_name}"

            )

        return self.providers[provider_name]

    # =====================================================
    # Current Time
    # =====================================================

    def now(self):

        return int(

            time.time()

        )

    # =====================================================
    # Provider Available
    # =====================================================

    def is_available(

        self,

        provider_name

    ):

        status = self.health[provider_name]

        if status["available"]:

            return True

        if self.now() >= status["retry_after"]:

            logger.info(

                f"{provider_name.upper()} cooldown expired."

            )

            status["available"] = True

            status["retry_after"] = 0

            return True

        return False

    # =====================================================
    # Disable Provider
    # =====================================================

    def disable_provider(

        self,

        provider_name,

        cooldown=600

    ):

        self.health[provider_name]["available"] = False

        self.health[provider_name]["retry_after"] = (

            self.now() + cooldown

        )

        logger.warning(

            f"{provider_name.upper()} disabled for "

            f"{cooldown} seconds."

        )

    # =====================================================
    # Statistics
    # =====================================================

    def add_success(

        self,

        provider_name,

        latency

    ):

        stats = self.statistics[provider_name]

        stats["success"] += 1

        stats["latency"].append(

            latency

        )

    def add_failure(

        self,

        provider_name

    ):

        self.statistics[provider_name]["failure"] += 1

    def add_retry(

        self,

        provider_name

    ):

        self.statistics[provider_name]["retry"] += 1

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        return {

            "priority": self.priority,

            "providers": self.health,

            "statistics": self.statistics

        }

    # =====================================================
    # Continue In Part-2
    # =====================================================

        # =====================================================
    # Reset Provider
    # =====================================================

    def reset_provider(

        self,

        provider_name

    ):

        provider_name = provider_name.lower()

        self.health[provider_name]["available"] = True

        self.health[provider_name]["retry_after"] = 0

        logger.info(

            f"{provider_name.upper()} is available again."

        )

    # =====================================================
    # Should Retry
    # =====================================================

    def should_retry(

        self,

        error

    ):

        text = str(error).lower()

        retry_errors = [

            "503",

            "timeout",

            "connection",

            "temporarily",

            "unavailable"

        ]

        return any(

            item in text

            for item in retry_errors

        )

    # =====================================================
    # Safe Invoke
    # =====================================================

    def safe_invoke(

        self,

        prompt,

        primary=None

    ):

        if primary:

            order = [

                primary.lower()

            ]

            for provider in self.priority:

                if provider not in order:

                    order.append(provider)

        else:

            order = self.priority.copy()

        last_exception = None

        for provider_name in order:

            if not self.is_available(

                provider_name

            ):

                logger.warning(

                    f"{provider_name.upper()} skipped (cooldown)."

                )

                continue

            provider = self.get_provider(

                provider_name

            )

            start = time.time()

            try:

                logger.info(

                    f"Trying {provider_name.upper()}..."

                )

                response = provider.invoke(

                    prompt

                )

                latency = round(

                    time.time() - start,

                    2

                )

                self.add_success(

                    provider_name,

                    latency

                )

                logger.info(

                    f"{provider_name.upper()} Success ({latency}s)"

                )

                return {

                    "provider": provider_name,

                    "response": response,

                    "latency": latency

                }

            except Exception as e:

                last_exception = e

                self.add_failure(

                    provider_name

                )

                message = str(e).lower()

                logger.error(

                    f"{provider_name.upper()} Failed : {e}"

                )

                # Authentication / Rate Limit
                if (

                    "401" in message

                    or "403" in message

                    or "429" in message

                ):

                    self.disable_provider(

                        provider_name

                    )

                    continue

                # Retry only for temporary errors
                if self.should_retry(

                    e

                ):

                    self.add_retry(

                        provider_name

                    )

                    try:

                        logger.info(

                            f"Retrying {provider_name.upper()}..."

                        )

                        response = provider.invoke(

                            prompt

                        )

                        latency = round(

                            time.time() - start,

                            2

                        )

                        self.add_success(

                            provider_name,

                            latency

                        )

                        return {

                            "provider": provider_name,

                            "response": response,

                            "latency": latency

                        }

                    except Exception as retry_error:

                        logger.error(

                            retry_error

                        )

                        self.add_failure(

                            provider_name

                        )

                        continue

                continue

        raise RuntimeError(

            f"All providers failed.\nLast Error : {last_exception}"

        )