from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.conversation import Conversation
from schemas.chat import CreateConversationRequest

router = APIRouter()


@router.post("/")
async def create_conversation(
    data: CreateConversationRequest,
    db: AsyncSession = Depends(get_db)
):

    conversation = Conversation(
        user_id=data.user_id,
        title="New Chat"
    )

    db.add(conversation)

    await db.commit()
    await db.refresh(conversation)

    return {
        "success": True,
        "conversation_id": str(conversation.id)
    }