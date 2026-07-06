"""
=========================================================
AI Lecture Assistant
Metadata API
=========================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from backend.api.responses import APIResponse
from backend.api.dependencies import get_metadata_service

from backend.utils.metadata_manager import MetadataManager


router = APIRouter(

    prefix="/metadata",

    tags=["Metadata"]

)
# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    service: MetadataManager = Depends(

        get_metadata_service

    )

):

    return APIResponse.success(

        message="Metadata Service Healthy",

        data=service.health_check()

    )

# ==========================================================
# List Lectures
# ==========================================================

@router.get("/lectures")
def list_lectures(

    service: MetadataManager = Depends(

        get_metadata_service

    )

):

    result = service.list_lectures()

    return APIResponse.success(

        message="Lectures fetched successfully.",

        data=result

    )


# ==========================================================
# Get Metadata
# ==========================================================

@router.get("/{lecture_id}")
def get_metadata(

    lecture_id: str,

    service: MetadataManager = Depends(

        get_metadata_service

    )

):

    result = service.load(

        lecture_id

    )

    return APIResponse.success(

        message="Metadata fetched successfully.",

        data=result

    )


# ==========================================================
# Delete Lecture
# ==========================================================

@router.delete("/{lecture_id}")
def delete_lecture(

    lecture_id: str,

    service: MetadataManager = Depends(

        get_metadata_service

    )

):

    result = service.delete_lecture(

        lecture_id

    )

    return APIResponse.success(

        message="Lecture deleted successfully.",

        data=result

    )


