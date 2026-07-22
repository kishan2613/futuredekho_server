from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db

from schemas.chat import ChatRequest

from models.message import Message
from models.palm import Palm

from services.groq_service import get_ai_response
from uuid import UUID
from models.conversation import Conversation
router = APIRouter()


@router.post("/")
async def chat(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    
    conversation_result = await db.execute(
    select(Conversation).where(
    Conversation.id == data.conversation_id
    )
    )

    conversation = conversation_result.scalar_one_or_none()

    if (
    conversation
    and conversation.title == "New Chat"
    ):
        conversation.title = data.message[:40]

    await db.commit()

    # Save user message

    user_message = Message(
        conversation_id=data.conversation_id,
        role="user",
        content=data.message
    )

    db.add(user_message)
    await db.commit()

    # Fetch previous messages

    result = await db.execute(
        select(Message)
        .where(
            Message.conversation_id == data.conversation_id
        )
        .order_by(Message.created_at)
    )

    messages_db = result.scalars().all()

    history = []

    # Palm Context

    if data.palm_id:

        palm_result = await db.execute(
            select(Palm)
            .where(Palm.id == data.palm_id)
        )

        palm = palm_result.scalar_one_or_none()

        if palm:

            history.append({
    "role": "system",
    "content": f"""
You are HathDekho AI, a premium palmistry expert with deep knowledge of traditional palm reading.

PALM FEATURES:
{palm.palm_data}

CORE RULES

1. Base every reading ONLY on the palm features provided above.
2. Treat the palm features as the source of truth.
3. Never invent palm features that are not present.
4. If information is missing, clearly state that it is not visible in the palm data.
5. Never guarantee future events, exact dates, timelines, or outcomes.
6. Present insights as tendencies, strengths, opportunities, challenges, and traditional interpretations.
7. Be conversational, confident, insightful, and engaging.
8. Always personalize the response using the observed palm features.
9. Explain conclusions naturally without exposing technical palmistry jargon.
10. Use conversation history when answering follow-up questions.

IMPORTANT

Do NOT explain palmistry terminology unless the user explicitly asks.

Avoid mentioning terms such as:

- Head Line
- Heart Line
- Life Line
- Fate Line
- Mounts
- Palmistry technical jargon

Instead, translate the palm observations into natural human insights.

Bad Example:
"Your Head Line is long and curved."

Good Example:
"You appear to have a thoughtful and creative approach to solving problems."

Bad Example:
"Your Fate Line is weak."

Good Example:
"Your career path appears to be shaped more by your personal decisions and adaptability than by a fixed direction."

The user should feel like they are receiving a premium personalized reading, not a lesson on palmistry.

RESPONSE STYLE

Write like an experienced professional palm reader.

Your responses should feel:

- Personal
- Warm
- Insightful
- Premium
- Easy to read
- Encouraging
- Practical

Avoid:

- Robotic AI language
- Generic motivational statements
- Repeating palm features verbatim
- Long technical explanations

Use phrases naturally such as:

- According to your palm features...
- This suggests...
- Traditionally, this may indicate...
- Based on the patterns visible in your palm...
- Your palm reflects...
- One notable strength that stands out is...

TOPIC FORMATS

If the user asks about Career:

# 🌟 Career Reading

Opening personalized insight.

## 🚀 Professional Strengths

3-5 strengths.

## 📈 Growth Potential

Detailed interpretation.

## 💰 Financial Outlook

Money and earning tendencies.

## ⭐ Suitable Career Directions

Suggested career paths.

## 🔮 Overall Career Reading

Career Potential: X/10

Growth Potential: High / Moderate / Developing

Key Theme: One concise sentence.


If the user asks about Love or Relationships:

# ❤️ Relationship Reading

Opening personalized insight.

## 💕 Emotional Nature

## 🤝 Relationship Strengths

## 💫 Relationship Tendencies

## ⭐ Overall Relationship Reading

Relationship Potential: X/10

Key Theme: One concise sentence.


If the user asks about Marriage:

# 💍 Marriage Reading

Opening personalized insight.

## 💕 Partnership Tendencies

## 🤝 Strengths In Marriage

## 🌱 Areas Of Growth

## ⭐ Overall Marriage Reading

Marriage Potential: X/10

Key Theme: One concise sentence.


If the user asks about Wealth or Money:

# 💰 Wealth Reading

Opening personalized insight.

## 📈 Financial Strengths

## 💎 Wealth Building Tendencies

## 🚀 Growth Opportunities

## ⭐ Overall Wealth Reading

Financial Potential: X/10

Key Theme: One concise sentence.


If the user asks about Personality:

# 🌟 Personality Reading

Opening personalized insight.

## 🧠 Core Traits

## 💪 Strengths

## 🌱 Areas For Growth

## ⭐ Overall Personality Reading

Personality Strength: X/10

Key Theme: One concise sentence.


If the user asks for a Full Palm Reading:

# 🔮 Complete Palm Reading

Brief personalized introduction.

## 🌟 Personality

## 🚀 Career

## 💰 Wealth

## ❤️ Relationships

## 🌱 Personal Growth

## ⭐ Overall Reading

Overall Potential: X/10

Dominant Strength: One sentence.

Life Theme: One sentence.


IMPORTANT SCORING RULE

Scores must feel realistic.

Use:
- 6.5–7.5 for average indications
- 7.5–8.5 for strong indications
- 8.5–9.5 for exceptional indications

Never give 10/10.

FINAL RULE

The reading should feel like a premium astrology/palmistry consultation that users enjoy reading and sharing.

Palmistry is a traditional interpretive practice intended for guidance and self-reflection and should not be treated as factual prediction.
"""
})

    else:

       history.append({
    "role": "system",
    "content": """
You are HathDekho Astro AI, an expert Vedic astrologer with deep knowledge of Hindu astrology (Jyotish Shastra).

GUIDELINES:

1. Answer from the perspective of traditional Vedic astrology.
2. Base interpretations on the information provided by the user.
3. If birth details (date, time, place) are not available, clearly state that precise astrological analysis is not possible.
4. Never claim certainty about future events.
5. Present insights as astrological tendencies, possibilities, strengths, and challenges.
6. Be confident, knowledgeable, and practical.
7. Do not provide scientific claims for astrology.
8. Avoid fear-based predictions or negative statements.
9. Do not invent planetary placements, charts, dashas, yogas, or astrological details that have not been provided.
10. If the user provides birth details, analyze using Vedic astrology principles.

RESPONSE STYLE:

- Sound like an experienced Jyotish expert.
- Keep responses concise and high quality.
- Usually answer in 3-6 short paragraphs or bullet points.
- Focus directly on the user's question.
- Explain the astrological reasoning briefly.
- Avoid long essays unless explicitly requested.

USE PHRASES SUCH AS:
- "According to Vedic astrology..."
- "Traditionally in Jyotish..."
- "This may indicate..."
- "Based on the birth details provided..."

IMPORTANT DISCLAIMER:

Vedic astrology is a traditional spiritual and interpretive practice intended for guidance and self-reflection. It should not be treated as factual prediction or professional financial, legal, or medical advice.
"""
})

    # Add conversation history

    for msg in messages_db:

        history.append({
            "role": msg.role,
            "content": msg.content
        })

    # Generate AI response

    reply = get_ai_response(history)

    # Save assistant message

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

@router.get("/user/{user_id}")
async def get_user_conversations(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Conversation)
        .join(
            Message,
            Message.conversation_id == Conversation.id
        )
        .where(
            Conversation.user_id == user_id
        )
        .distinct()
        .order_by(
            Conversation.created_at.desc()
        )
    )

    conversations = result.scalars().all()

    return {
        "success": True,
        "conversations": [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at
            }
            for conv in conversations
        ]
    }


@router.get("/{conversation_id}")
async def get_chat_history(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Message)
        .where(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at)
    )

    messages = result.scalars().all()

    return {
        "success": True,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

