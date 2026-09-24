import json
import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from groq import Groq

router = APIRouter(prefix="/baby-names", tags=["Baby Names"])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Use a currently available Groq model from your account.
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


class BabyNameRequest(BaseModel):
    surname: Optional[str] = ""
    gender: str = Field(..., description="boy, girl, or unisex")

    birth_date: Optional[str] = ""
    birth_time: Optional[str] = ""
    birth_place: Optional[str] = ""

    preferred_letter: Optional[str] = ""
    preferred_syllable: Optional[str] = ""

    style: Optional[str] = "traditional"
    meaning_preference: Optional[str] = ""

    name_count: int = Field(default=10, ge=5, le=20)


SYSTEM_PROMPT = """
You are HathDekho Baby Name Agent.

You specialize in:
- Vedic Astrology
- Hindu Numerology
- Traditional Indian naming practices
- Sanskrit and Indian names
- Indian name meanings
- Name-number analysis

Your task is to help parents discover meaningful and potentially auspicious
names for their upcoming child.

IMPORTANT:

This is a traditional/spiritual naming interpretation.
Do not present astrology or numerology as scientifically proven.
Never guarantee that a name will cause wealth, health, success, longevity,
marriage, or any other real-world outcome.

Do not fabricate astrology information.

If birth date, time, or place are incomplete, do not invent:
- Nakshatra
- Rashi
- Pada
- Moon sign
- Ascendant
- Planetary positions
- Lucky syllables

Only use astrology-specific information when it is actually provided or
reliably calculated by another service.

NAME QUALITY:

Every name must:
- Be a plausible real Indian name
- Have a meaningful interpretation
- Have a reasonable origin
- Be pronounceable
- Match the requested gender
- Match the requested style
- Avoid fabricated Sanskrit
- Avoid offensive or inappropriate meanings
- Avoid repetitive recommendations

Generate more candidates internally than you return.

Consider:
1. Baby gender
2. Preferred starting letter
3. Preferred starting syllable
4. Family surname
5. Name meaning
6. Indian/Sanskrit linguistic roots
7. Traditional naming considerations
8. Numerological name number when possible
9. Pronunciation
10. Modern/traditional preference
11. Uniqueness

Do not choose names purely because of a numerical score.

STYLE:

The experience should feel:
- Warm
- Magical
- Personal
- Elegant
- Exciting
- Indian/Vedic

Use phrases such as:
"traditionally associated with..."
"aligns with the selected naming criteria"
"carries symbolism associated with..."

Avoid:
"This name guarantees success."
"This name will make your child wealthy."
"This name will prevent problems."

OUTPUT:

Return ONLY valid JSON.

No Markdown.
No ```json.
No explanation outside JSON.

Use exactly this structure:

{
  "success": true,
  "message": "",
  "baby_profile": {
    "gender": "",
    "birth_date": "",
    "birth_time": "",
    "birth_place": "",
    "preferred_letter": "",
    "preferred_syllable": "",
    "style": "",
    "meaning_preference": ""
  },
  "naming_basis": {
    "astrology_used": false,
    "numerology_used": true,
    "preferred_letter_used": false,
    "family_name_considered": false,
    "explanation": ""
  },
  "recommendations": [
    {
      "rank": 1,
      "name": "",
      "meaning": "",
      "origin": "",
      "gender": "",
      "name_number": 0,
      "starting_letter": "",
      "lucky_number": 0,
      "why_suggested": "",
      "personality_association": "",
      "pronunciation": "",
      "family_name_fit": ""
    }
  ],
  "top_pick": {
    "name": "",
    "meaning": "",
    "reason": ""
  },
  "name_themes": [],
  "parent_note": ""
}

RULES:

- Return exactly the requested number of recommendations.
- If name_count is not specified, return 10.
- name_number must be numeric.
- lucky_number must be numeric.
- If a number cannot be reliably calculated, use 0.
- If a preferred letter exists, prioritize that letter.
- If a preferred syllable exists, prioritize that syllable.
- If a surname exists, consider the complete name.
- If a meaning preference exists, prioritize that meaning.
"""


@router.post("/generate")
async def generate_baby_names(request: BabyNameRequest):

    user_prompt = f"""
Generate baby name recommendations using these details:

Surname:
{request.surname or "Not provided"}

Gender:
{request.gender}

Birth date:
{request.birth_date or "Not provided"}

Birth time:
{request.birth_time or "Not provided"}

Birth place:
{request.birth_place or "Not provided"}

Preferred starting letter:
{request.preferred_letter or "Not provided"}

Preferred starting syllable:
{request.preferred_syllable or "Not provided"}

Name style:
{request.style or "traditional"}

Meaning/theme preference:
{request.meaning_preference or "Not provided"}

Number of names:
{request.name_count}

Generate exactly {request.name_count} strong recommendations.

Remember:
- Do not invent astrology data.
- Prefer authentic Indian names.
- Consider the surname if provided.
- Make each recommendation meaningfully different.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.7,
            max_tokens=5000,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        content = response.choices[0].message.content

        if not content:
            raise HTTPException(
                status_code=500,
                detail="AI returned an empty response."
            )

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="AI returned invalid JSON."
            )

        # Basic validation
        if "recommendations" not in result:
            raise HTTPException(
                status_code=500,
                detail="Invalid AI response."
            )

        recommendations = result["recommendations"]

        # Keep API output consistent with requested amount
        result["recommendations"] = recommendations[:request.name_count]

        result["success"] = True

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Baby name generation error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Could not generate baby names. Please try again."
        )