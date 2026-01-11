from pydantic import BaseModel


class ImageBase(BaseModel):
    file_path: str


class ImageCreate(ImageBase):
    pass


class ImageRead(ImageBase):
    id: str
    listing_id: str

    class Config:
        orm_mode = True
