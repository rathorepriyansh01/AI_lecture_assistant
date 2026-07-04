"""
=========================================================
AI Lecture Assistant
Common API Responses
=========================================================
"""

from typing import Any, Optional
from fastapi.responses import JSONResponse


class APIResponse:
    """
    Common Response Builder
    """

    @staticmethod
    def success(

        message: str,

        data: Optional[Any] = None,

        status_code: int = 200

    ) -> JSONResponse:

        return JSONResponse(

            status_code=status_code,

            content={

                "success": True,

                "message": message,

                "data": data

            }

        )

    @staticmethod
    def error(

        message: str,

        status_code: int = 400,

        errors: Optional[Any] = None

    ) -> JSONResponse:

        return JSONResponse(

            status_code=status_code,

            content={

                "success": False,

                "message": message,

                "errors": errors

            }

        )