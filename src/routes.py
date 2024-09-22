from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import current_active_user
from decorators.retry_dec import async_retry
from main import app
from src.book_schemas.input import BookCreate
from src.book_schemas.output import BookResponse, BooksResponse
from src.database import get_db
from src.repositories.book_repository import BookRepository


@app.get("/protected-route", tags=["Protected"])
async def protected_route(user = Depends(current_active_user)):
    return {"message": f"Привет, {user.username}"}


@async_retry(times=5, delay=2, exceptions=(HTTPException,))
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    new_book = book_repo.create(book.title, book.author, book.publication_date)
    return new_book.as_dict()


@async_retry(times=5, delay=2, exceptions=(HTTPException,))
@app.get("/books/", response_model=BooksResponse)
def get_books(db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    books = book_repo.get_all()
    return books


@async_retry(times=5, delay=2, exceptions=(HTTPException,))
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    book = book_repo.get_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book.as_dict()


@async_retry(times=5, delay=2, exceptions=(HTTPException,))
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    updated_book = book_repo.update(book_id, book_data.title, book_data.author, book_data.publication_date)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return updated_book


@async_retry(times=5, delay=2, exceptions=(HTTPException,))
@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    success = book_repo.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"message": "Книга успешно удалена"}
