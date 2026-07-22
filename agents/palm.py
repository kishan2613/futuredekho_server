from google import genai
from PIL import Image
import json
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_palm_features(image_path):

    image = Image.open(image_path)

    prompt = """
    You are a professional palm feature extraction system.

Analyze the uploaded palm image.

Return ONLY valid JSON.

Do not predict personality.
Do not predict future.
Do not perform palm reading.

Extract:

1. Hand Type
2. Life Line
   - length
   - depth
   - continuity
   - branches

3. Heart Line
   - length
   - depth
   - continuity
   - ending

4. Head Line
   - length
   - depth
   - continuity
   - start_point
   - curvature

5. Fate Line
   - presence
   - depth
   - continuity
   - start_point

6. Mounts
   - Jupiter
   - Saturn
   - Apollo
   - Mercury
   - Venus
   - Moon
   - Mars Positive
   - Mars Negative

7. Major markings
   - star
   - cross
   - triangle
   - square
   - island

8. Confidence

Return ONLY JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text