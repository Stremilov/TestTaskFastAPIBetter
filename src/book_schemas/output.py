from typing import List

from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publication_date: str


class BooksResponse(BaseModel):
    books: List[BookResponse]
