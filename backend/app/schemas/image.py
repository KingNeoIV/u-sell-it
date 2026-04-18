from pydantic import BaseModel
from uuid import UUID

class ImageRead(BaseModel):
    """
    Schema returned when reading image records.

    Represents a stored image associated with a listing, including its
    unique identifier, the parent listing's UUID, and the file path
    where the image is stored. Configured for ORM compatibility.
    """

    id: UUID
    listing_id: UUID
    file_path: str

    # Enable ORM mode so SQLAlchemy models can be serialized directly.
    model_config = {"from_attributes": True}
