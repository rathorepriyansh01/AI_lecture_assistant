"""
=========================================================
AI Lecture Assistant
Notes API
=========================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel

from backend.api.responses import APIResponse
from backend.api.dependencies import get_notes_service

from backend.services.notes_service import NotesService


router = APIRouter(

    prefix="/notes",

    tags=["Notes"]

)


# ==========================================================
# Request Model
# ==========================================================

class NotesRequest(BaseModel):

    lecture_id: str

    notes_type: str = "detailed"

    use_cache: bool = True


# ==========================================================
# Generate Notes
# ==========================================================

@router.post("/")
def generate_notes(

    request: NotesRequest,

    service: NotesService = Depends(

        get_notes_service

    )

):

    result = service.generate(

        lecture_id=request.lecture_id,

        notes_type=request.notes_type,

        use_cache=request.use_cache

    )

    return APIResponse.success(

        message="Notes generated successfully.",

        data=result

    )


# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    service: NotesService = Depends(

        get_notes_service

    )

):

    return APIResponse.success(

        message="Notes Service Healthy",

        data=service.health_check()

    )