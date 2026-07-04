"""
=========================================================
AI Lecture Assistant
Base Provider
=========================================================

All LLM Providers must inherit this class.

Supported Providers

✓ Gemini
✓ Groq
✓ NVIDIA
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseProvider(ABC):

    """
    Base class for every LLM provider.

    Every provider must implement:

        invoke()
        health_check()

    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int
    ):

        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    # =====================================================
    # Invoke
    # =====================================================

    @abstractmethod
    def invoke(
        self,
        prompt: str
    ) -> str:
        """
        Generate response from LLM.

        Returns
        -------
        str
            Model response.
        """
        pass

    # =====================================================
    # Health Check
    # =====================================================

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Returns provider information.

        Example
        -------
        {
            "status": "healthy",
            "provider": "Gemini",
            "model": "...",
            "temperature": 0.2,
            "max_tokens": 4096
        }
        """
        pass

    # =====================================================
    # Provider Info
    # =====================================================

    def info(self) -> Dict[str, Any]:

        return {

            "provider": self.__class__.__name__,

            "model": self.model,

            "temperature": self.temperature,

            "max_tokens": self.max_tokens

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return (

            f"{self.__class__.__name__}("

            f"model='{self.model}', "

            f"temperature={self.temperature}, "

            f"max_tokens={self.max_tokens})"

        )