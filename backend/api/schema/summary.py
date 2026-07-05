"""
=========================================================
AI Lecture Assistant
Summary API
=========================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel

from backend.api.responses import APIResponse
from backend.api.dependencies import get_summary_service

from backend.services.summary_service import SummaryService


router = APIRouter(

    prefix="/summary",

    tags=["Summary"]

)


# ==========================================================
# Request Model
# ==========================================================

class SummaryRequest(BaseModel):

    lecture_id: str

    summary_type: str = "detailed"

    use_cache: bool = True


# ==========================================================
# Generate Summary
# ==========================================================

@router.post("/")
def generate_summary(

    request: SummaryRequest,

    service: SummaryService = Depends(

        get_summary_service

    )

):

    result = service.generate(

        lecture_id=request.lecture_id,

        summary_type=request.summary_type,

        use_cache=request.use_cache

    )

    return APIResponse.success(

        message="Summary generated successfully.",

        data=result

    )


# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    service: SummaryService = Depends(

        get_summary_service

    )

):

    return APIResponse.success(

        message="Summary Service Healthy",

        data=service.health_check()

    )