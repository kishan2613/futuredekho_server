import cloudinary.uploader

async def upload_image(filepath):
    result = cloudinary.uploader.upload(
        filepath,
        folder="futuredekho/palms"
    )

    return result["secure_url"]