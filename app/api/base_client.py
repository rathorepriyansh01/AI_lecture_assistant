"""
=========================================================
AI Lecture Assistant
Base API Client
=========================================================

Central HTTP Client for all frontend API calls.

Every API wrapper should use this client.
"""

import requests
import logging

from config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)


class BaseAPIClient:

    def __init__(self):

        self.base_url = API_BASE_URL.rstrip("/")

        self.timeout = REQUEST_TIMEOUT

    # =====================================================
    # Build URL
    # =====================================================

    def build_url(
        self,
        endpoint: str
    ):

        endpoint = endpoint.lstrip("/")

        return f"{self.base_url}/{endpoint}"

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        endpoint,
        **kwargs
    ):

        response = requests.get(

            self.build_url(endpoint),

            timeout=self.timeout,

            **kwargs

        )

        return self._handle_response(response)

    # =====================================================
    # POST
    # =====================================================

    def post(
        self,
        endpoint,
        **kwargs
    ):

        response = requests.post(

            self.build_url(endpoint),

            timeout=self.timeout,

            **kwargs

        )

        return self._handle_response(response)

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        endpoint,
        **kwargs
    ):

        response = requests.delete(

            self.build_url(endpoint),

            timeout=self.timeout,

            **kwargs

        )

        return self._handle_response(response)

    # =====================================================
    # Response Handler
    # =====================================================

    def _handle_response(
        self,
        response
    ):

        try:

            data = response.json()

        except Exception:

            response.raise_for_status()

            return {}

        if response.status_code >= 400:

            message = data.get(

                "message",

                "Unknown API Error"

            )

            raise RuntimeError(message)

        return data