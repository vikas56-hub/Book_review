from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    content: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        from_attributes = True
