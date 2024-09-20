from sqlalchemy.orm import Session
from src.models import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, author: str, publication_date: str) -> Book:
        new_book = Book(title=title, author=author, publication_date=publication_date)
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def get_all(self):
        return self.db.query(Book).all()

    def get_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update(self, book_id: int, title: str, author: str, publication_date: str):
        book = self.get_by_id(book_id)
        if book:
            book.title = title
            book.author = author
            book.publication_date = publication_date
            self.db.commit()
            self.db.refresh(book)
        return book

    # Удаление книги
    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
