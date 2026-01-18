from pydantic import BaseModel


# Base schema shared by all image-related models.
# Represents the stored file path for an image.
class ImageBase(BaseModel):
    file_path: str


# Schema used when creating a new image entry.
# Inherits all fields from ImageBase.
class ImageCreate(ImageBase):
    pass


# Schema returned when reading image data from the database.
# Includes indentifiers and enables ORM compatibility.
class ImageRead(ImageBase):
    # Unique identifier for the image.
    id: str

    # ID of the listing this image belongs to.
    listing_id: str

    model_config = {"from_attributes": True}
