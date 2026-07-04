"""
=========================================================
AI Lecture Assistant
Middleware
=========================================================
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every API request and response time.
    """

    async def dispatch(

        self,

        request,

        call_next

    ):

        start = time.time()

        response = await call_next(

            request

        )

        execution_time = round(

            time.time() - start,

            2

        )

        logger.info(

            f"{request.method} "

            f"{request.url.path} "

            f"{response.status_code} "

            f"{execution_time}s"

        )

        response.headers[

            "X-Execution-Time"

        ] = str(execution_time)

        return response