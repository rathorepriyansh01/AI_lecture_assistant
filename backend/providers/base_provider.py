"""
=========================================================
AI Lecture Assistant
Base Provider
=========================================================
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    """
    Base class for all LLM providers.

    Every provider must implement these methods.
    """

    def __init__(

        self,

        api_key,

        model,

        temperature=0.2,

        max_tokens=2048

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

    ):

        """
        Send prompt to the model
        """

        pass

    # =====================================================
    # Health Check
    # =====================================================

    @abstractmethod
    def health_check(self):

        pass

    # =====================================================
    # Provider Info
    # =====================================================

    def provider_info(self):

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

            f"{self.__class__.__name__}"

            f"(model={self.model})"

        )