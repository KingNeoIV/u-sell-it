from pydantic import BaseModel
from uuid import UUID

class ImageRead(BaseModel):
    id: UUID
    listing_id: UUID
    file_path: str

    model_config = {"from_attributes": True}
