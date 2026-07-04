"""
=========================================================
AI Lecture Assistant
Chat API
=========================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from pydantic import BaseModel, Field

from backend.api.responses import APIResponse
from backend.api.dependencies import get_chat_service

from backend.services.chatbot_service import ChatbotService


router = APIRouter(

    prefix="/chat",

    tags=["Chat"]

)


# ==========================================================
# Request Model
# ==========================================================

class ChatRequest(BaseModel):

    lecture_id: str

    question: str = Field(

        min_length=1,

        max_length=2000

    )

    use_cache: bool = True


# ==========================================================
# Chat With Lecture
# ==========================================================

@router.post("/")
def chat(

    request: ChatRequest,

    service: ChatbotService = Depends(

        get_chat_service

    )

):

    result = service.ask(

        lecture_id=request.lecture_id,

        question=request.question,

        use_cache=request.use_cache

    )

    return APIResponse.success(

        message="Response generated successfully.",

        data=result

    )


# ==========================================================
# Health Check
# ==========================================================

@router.get("/health")
def health(

    service: ChatbotService = Depends(

        get_chat_service

    )

):

    return APIResponse.success(

        message="Chat Service Healthy",

        data=service.health_check()

    )