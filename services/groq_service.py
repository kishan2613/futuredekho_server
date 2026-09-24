from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def get_ai_response(messages):

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content


def generate_kundli_report(chart_data):

    messages = [
        {
            "role": "system",
            "content": """
You are HathDekho Astro AI.

You are an expert Vedic astrologer.

IMPORTANT RULES

The planetary calculations are already done.

Never calculate astrology.

Never invent planetary positions.

Interpret ONLY the supplied JSON.

Explain naturally.

Return markdown.

Sections:

# 🌟 Personality

# 💼 Career

# ❤️ Marriage

# 💰 Wealth

# 🏥 Health

# 👨‍👩‍👧 Relationships

# 🌱 Strengths

# ⚠️ Challenges

# 🍀 Lucky Elements

Lucky Color

Lucky Number

Lucky Day

Lucky Direction

# 🪔 Remedies

# ⭐ Overall Reading

Overall Potential : X/10

Life Theme :
"""
        },
        {
            "role": "user",
            "content": str(chart_data)
        }
    ]

    return get_ai_response(messages)