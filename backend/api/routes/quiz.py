"""
=========================================================
AI Lecture Assistant
Quiz API
=========================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel, Field

from backend.api.responses import APIResponse
from backend.api.dependencies import get_quiz_service

from backend.services.quiz_service import QuizService


router = APIRouter(

    prefix="/quiz",

    tags=["Quiz"]

)


# ==========================================================
# Request Model
# ==========================================================

class QuizRequest(BaseModel):

    lecture_id: str

    difficulty: str = Field(

        default="medium",

        pattern="^(easy|medium|hard)$"

    )

    total_questions: int = Field(

        default=20,

        ge=1,

        le=100

    )

    use_cache: bool = True


# ==========================================================
# Generate Quiz
# ==========================================================

@router.post("/")
def generate_quiz(

    request: QuizRequest,

    service: QuizService = Depends(

        get_quiz_service

    )

):

    result = service.generate(

        lecture_id=request.lecture_id,

        difficulty=request.difficulty,

        total_questions=request.total_questions,

        use_cache=request.use_cache

    )

    return APIResponse.success(

        message="Quiz generated successfully.",

        data=result

    )


# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    service: QuizService = Depends(

        get_quiz_service

    )

):

    return APIResponse.success(

        message="Quiz Service Healthy",

        data=service.health_check()

    )