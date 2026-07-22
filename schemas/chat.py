from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class CreateConversationRequest(BaseModel):
    user_id: UUID


class ChatRequest(BaseModel):
    conversation_id: UUID
    message: str
    palm_id: Optional[int] = None