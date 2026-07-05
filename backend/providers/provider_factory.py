"""
=========================================================
AI Lecture Assistant
Provider Factory
=========================================================

STATUS : FINAL
Version : 1.0
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
    THIRD_PROVIDER,
    MAX_RETRY,
    PROVIDER_COOLDOWN,
)

from backend.providers.gemini_provider import GeminiProvider
from backend.providers.groq_provider import GroqProvider
from backend.providers.nvidia_provider import NvidiaProvider

logger = logging.getLogger(__name__)


class ProviderFactory:

    def __init__(self):

        logger.info("=" * 70)
        logger.info("Initializing Provider Factory...")
        logger.info("=" * 70)

        self._lock = Lock()

        # ==========================================
        # Lazy Provider Cache
        # ==========================================

        self.providers = {}

        # ==========================================
        # Provider Priority
        # ==========================================

        self.priority = [

            PRIMARY_PROVIDER.lower(),

            SECONDARY_PROVIDER.lower(),

            THIRD_PROVIDER.lower()

        ]

        # ==========================================
        # Health Cache
        # ==========================================

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

        # ==========================================
        # Statistics
        # ==========================================

        self.statistics = {

            provider: {

                "success": 0,

                "failure": 0,

                "retry": 0,

                "calls": 0,

                "latency": []

            }

            for provider in [

                "gemini",

                "groq",

                "nvidia"

            ]

        }

        logger.info("Provider Factory Ready.")

    # =====================================================
    # Current Time
    # =====================================================

    def now(self):

        return int(time.time())

    # =====================================================
    # Create Provider
    # =====================================================

    def _create_provider(

        self,

        provider_name

    ):

        provider_name = provider_name.lower()

        if provider_name == "gemini":

            return GeminiProvider(

                api_key=GEMINI_API_KEY,

                model=GEMINI_MODEL,

                temperature=TEMPERATURE,

                max_tokens=MAX_TOKENS

            )

        if provider_name == "groq":

            return GroqProvider(

                api_key=GROQ_API_KEY,

                model=GROQ_MODEL,

                temperature=TEMPERATURE,

                max_tokens=MAX_TOKENS

            )

        if provider_name == "nvidia":

            return NvidiaProvider(

                api_key=NVIDIA_API_KEY,

                model=NVIDIA_MODEL,

                temperature=TEMPERATURE,

                max_tokens=MAX_TOKENS

            )

        raise ValueError(

            f"Unknown provider : {provider_name}"

        )

    # =====================================================
    # Get Provider (Lazy Loading)
    # =====================================================

    def get_provider(

        self,

        provider_name

    ):

        provider_name = provider_name.lower()

        with self._lock:

            if provider_name not in self.providers:

                logger.info(

                    f"Loading {provider_name.upper()} Provider..."

                )

                self.providers[provider_name] = (

                    self._create_provider(

                        provider_name

                    )

                )

        return self.providers[provider_name]

    # =====================================================
    # Availability
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

        cooldown=PROVIDER_COOLDOWN

    ):

        provider_name = provider_name.lower()

        self.health[provider_name]["available"] = False

        self.health[provider_name]["retry_after"] = (

            self.now() + cooldown

        )

        logger.warning(

            f"{provider_name.upper()} disabled "

            f"for {cooldown} seconds."

        )

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

            f"{provider_name.upper()} reset successfully."

        )

    # =====================================================
    # Retry Policy
    # =====================================================

    def should_retry(

        self,

        error

    ):

        message = str(error).lower()

        retry_keywords = [

            "503",

            "timeout",

            "connection",

            "temporarily",

            "unavailable",

            "network"

        ]

        return any(

            keyword in message

            for keyword in retry_keywords

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

        stats["calls"] += 1

        stats["latency"].append(

            latency

        )

    def add_failure(

        self,

        provider_name

    ):

        stats = self.statistics[provider_name]

        stats["failure"] += 1

        stats["calls"] += 1

    def add_retry(

        self,

        provider_name

    ):

        self.statistics[provider_name]["retry"] += 1

    # =====================================================
    # Health Check
    # =====================================================

    def health_check(self):

        report = {}

        for provider in self.priority:

            report[provider] = {

                "available": self.health[provider]["available"],

                "cooldown":

                    max(

                        0,

                        self.health[provider]["retry_after"]

                        - self.now()

                    ),

                "statistics":

                    self.statistics[provider]

            }

        return report

    # =====================================================
    # Provider Statistics
    # =====================================================

    def get_statistics(self):

        output = {}

        for provider, stats in self.statistics.items():

            latency = stats["latency"]

            average_latency = (

                round(

                    sum(latency) / len(latency),

                    2

                )

                if latency

                else 0

            )

            output[provider] = {

                "calls": stats["calls"],

                "success": stats["success"],

                "failure": stats["failure"],

                "retry": stats["retry"],

                "average_latency": average_latency

            }

        return output

    # =====================================================
    # Clear Statistics
    # =====================================================

    def clear_statistics(self):

        for provider in self.statistics:

            self.statistics[provider] = {

                "success": 0,

                "failure": 0,

                "retry": 0,

                "calls": 0,

                "latency": []

            }

        logger.info(

            "Provider statistics cleared."

        )
    # =====================================================
    # Safe Invoke
    # =====================================================

    def safe_invoke(

        self,

        prompt,

        primary=None

    ):

        # ---------------------------------------------
        # Build Provider Order
        # ---------------------------------------------

        if primary:

            order = [primary.lower()]

            for provider in self.priority:

                if provider not in order:

                    order.append(provider)

        else:

            order = self.priority.copy()

        last_exception = None

        # ---------------------------------------------
        # Try Providers
        # ---------------------------------------------

        for provider_name in order:

            if not self.is_available(provider_name):

                logger.warning(

                    f"{provider_name.upper()} skipped "

                    "(cooldown active)."

                )

                continue

            provider = self.get_provider(

                provider_name

            )

            retries = 0

            for retries in range(MAX_RETRY + 1):

                start = time.time()

                try:

                    logger.info(
                        f"Trying "
                        f"{provider_name.upper()} "
                        f"(Attempt {retries + 1})"
                    )

                    # ============================
                    # Invoke Provider
                    # ============================

                    response = provider.invoke(
                        prompt
                    )

                    if not response:

                        raise RuntimeError(
                            "Empty response received."
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
                        f"{provider_name.upper()} "
                        f"Success "
                        f"({latency}s)"
                    )

                    return {
                        "provider": provider_name,
                        "response": response,
                        "latency": latency
                    }

                except Exception as e:

                    last_exception = e

                    retries += 1

                    self.add_failure(

                        provider_name

                    )

                    message = str(e).lower()

                    logger.error(

                        f"{provider_name.upper()} "

                        f"Failed : {e}"

                    )

                    # ---------------------------------
                    # Authentication Errors
                    # ---------------------------------

                    if (

                        "401" in message

                        or "403" in message

                    ):

                        logger.error(

                            f"{provider_name.upper()} "

                            "Authentication Failed."

                        )

                        self.disable_provider(

                            provider_name

                        )

                        break

                    # ---------------------------------
                    # Rate Limit
                    # ---------------------------------

                    if "429" in message:

                        logger.warning(

                            f"{provider_name.upper()} "

                            "Rate Limit Reached."

                        )

                        self.disable_provider(

                            provider_name

                        )

                        break

                    # ---------------------------------
                    # Retry
                    # ---------------------------------

                    if self.should_retry(e):

                        if retries < MAX_RETRY:

                            self.add_retry(provider_name)

                            logger.info(

                            f"Retrying {provider_name.upper()}..."

                            )

                            continue

                        logger.warning(

                            f"{provider_name.upper()} Retry Limit Reached."

                            )

                    # ---------------------------------
                    # Unknown Error
                    # ---------------------------------

                    break

        # ---------------------------------------------
        # All Providers Failed
        # ---------------------------------------------

        raise RuntimeError(

            "All LLM Providers Failed.\n\n"

            f"Last Error:\n{last_exception}"

        )