from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.palm import Palm
from database import get_db
from schemas.chat import ChatRequest
from models.message import Message
from services.groq_service import get_ai_response

router = APIRouter()


@router.post("/")
async def chat(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db)
):

    # Save user message

    user_message = Message(
        conversation_id=data.conversation_id,
        role="user",
        content=data.message
    )

    db.add(user_message)
    await db.commit()

    # Load history

    result = await db.execute(
        select(Message)
        .where(
            Message.conversation_id == data.conversation_id
        )
        .order_by(Message.created_at)
    )

    messages = result.scalars().all()

    history = []

    for msg in messages:
        history.append({
            "role": msg.role,
            "content": msg.content
        })

    # Get AI response

    reply = get_ai_response(history)

    # Save assistant response

    assistant_message = Message(
        conversation_id=data.conversation_id,
        role="assistant",
        content=reply
    )

    db.add(assistant_message)
    await db.commit()

    return {
        "success": True,
        "reply": reply
    }