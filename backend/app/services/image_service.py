import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.db.models.image import Image

UPLOAD_DIR = "uploads"


class ImageService:
    def __init__(self, db: Session):
        self.db = db

    def add_image(self, listing_id: str, file: UploadFile):
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Build a safe file path
        save_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file to disk
        with open(save_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Create DB entry
        image = Image(
            listing_id=listing_id,
            file_path=save_path
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)

        return image
