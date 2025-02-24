from fastapi import APIRouter, Depends
from services.auth_service import get_current_user
from services.chat_service import ChatService

router = APIRouter()

@router.post("/chat")
async def chat(
    message: str,
    chat_service: ChatService = Depends(),
    current_user = Depends(get_current_user)
):
    response = await chat_service.process_message(
        user_id=current_user.id,
        message=message
    )
    return {"response": response} 