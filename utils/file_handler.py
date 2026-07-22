import os
import uuid


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


async def save_image(file):

    extension = file.filename.split(".")[-1]

    filename = (
        f"{uuid.uuid4()}.{extension}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as f:

        f.write(
            await file.read()
        )

    return filepath