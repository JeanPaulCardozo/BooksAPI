from pydantic import BaseModel
from typing import Optional


class BookSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    author: str
    price: float
    yearrelease: int
    user_id: int

    class Config:
        from_attributes = True


class AddUpdateBookSchema(BaseModel):
    title: str
    description: Optional[str] = None
    author: str
    price: float
    yearrelease: int

    class Config:
        from_attributes = True
