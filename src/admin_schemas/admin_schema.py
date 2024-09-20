from sqladmin import ModelView

from src.models import Book


class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.author, Book.publication_date]
