from fastapi import APIRouter, Depends
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/chat", tags=["Chat"])

# Instantiate the service
gemini_service = GeminiService()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response_text = await gemini_service.generate_response(
        user_id=request.user_id,
        prompt=request.message
    )
    return ChatResponse(response=response_text)
