from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def get_ai_response(messages):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return completion.choices[0].message.content