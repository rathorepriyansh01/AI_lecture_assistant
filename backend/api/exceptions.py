"""
=========================================================
AI Lecture Assistant
Global Exception Handlers
=========================================================
"""

import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# ==========================================================
# Register Exception Handlers
# ==========================================================

def register_exception_handlers(app: FastAPI):

    # ------------------------------------------------------
    # Validation Error
    # ------------------------------------------------------

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(

        request: Request,

        exc: RequestValidationError

    ):

        return JSONResponse(

            status_code=422,

            content={

                "success": False,

                "message": "Validation Error",

                "errors": exc.errors()

            }

        )

    # ------------------------------------------------------
    # File Not Found
    # ------------------------------------------------------

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(

        request: Request,

        exc: FileNotFoundError

    ):

        return JSONResponse(

            status_code=404,

            content={

                "success": False,

                "message": str(exc)

            }

        )

    # ------------------------------------------------------
    # Value Error
    # ------------------------------------------------------

    @app.exception_handler(ValueError)
    async def value_error_handler(

        request: Request,

        exc: ValueError

    ):

        return JSONResponse(

            status_code=400,

            content={

                "success": False,

                "message": str(exc)

            }

        )

    # ------------------------------------------------------
    # Runtime Error
    # ------------------------------------------------------

    @app.exception_handler(RuntimeError)
    async def runtime_error_handler(

        request: Request,

        exc: RuntimeError

    ):

        logger.exception(exc)

        return JSONResponse(

            status_code=500,

            content={

                "success": False,

                "message": str(exc)

            }

        )

    # ------------------------------------------------------
    # Unknown Error
    # ------------------------------------------------------

    @app.exception_handler(Exception)
    async def general_exception_handler(

        request: Request,

        exc: Exception

    ):

        logger.exception(exc)

        return JSONResponse(

            status_code=500,

            content={

                "success": False,

                "message": "Internal Server Error"

            }

        )