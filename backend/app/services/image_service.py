import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.db.models.image import Image
from app.core.config import settings

UPLOAD_DIR = "uploads"

# Map MIME types to proper file extensions
MIME_TO_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
    "image/x-icon": ".ico",
    "image/vnd.microsoft.icon": ".ico",
    "image/heic": ".heic",
    "image/heif": ".heif",
    "image/avif": ".avif"
}

class ImageService:
    def __init__(self, db: Session):
        self.db = db

    async def add_image(self, listing_id: str, file: UploadFile):
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Validate MIME type
        if file.content_type not in MIME_TO_EXT:
            raise ValueError("Unsupported file type")

        # Determine extension from MIME type
        ext = MIME_TO_EXT[file.content_type]

        # Generate safe UUID filename
        new_filename = f"{uuid.uuid4()}{ext}"

        # Build final save path
        save_path = os.path.join(UPLOAD_DIR, new_filename)

        # Save file to disk
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())

        # Build public URL for frontend
        public_url = f"{settings.backend_url}/uploads/{new_filename}"

        # Create DB entry
        image = Image(
            listing_id=listing_id,
            file_path=public_url
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)

        return image

    def get_image_by_id(self, image_id: str):
        return self.db.query(Image).filter(Image.id == image_id).first()

    def delete_image(self, image_id: str):
        image = self.get_image_by_id(image_id)
        if image:
            self.db.delete(image)
            self.db.commit()
