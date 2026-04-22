import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.db.models.image import Image

UPLOAD_DIR = "uploads"


class ImageService:
    def __init__(self, db: Session):
        self.db = db

    async def add_image(self, listing_id: str, file: UploadFile):
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Extract and validate extension
        _, ext = os.path.splitext(file.filename)
        ext = ext.lower()

        allowed_exts = {".png", ".jpg", ".jpeg"}
        if ext not in allowed_exts:
            raise ValueError("Unsupported file type")

        # Generate safe UUID filename
        new_filename = f"{uuid.uuid4()}{ext}"

        # Build final save path
        save_path = os.path.join(UPLOAD_DIR, new_filename)

        # Save file to disk
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())

        # Create DB entry
        image = Image(
            listing_id=listing_id,
            file_path=save_path
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)

        return image
    
    # Retrieve an image by its ID
    def get_image_by_id(self, image_id: str):
        return self.db.query(Image).filter(Image.id == image_id).first()

    # Delete an image by its ID, including the file on disk
    def delete_image(self, image_id: str):
        image = self.get_image_by_id(image_id)
        if image:
            self.db.delete(image)
            self.db.commit()
