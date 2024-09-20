from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_date = Column(Date)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_date": self.publication_date.isoformat() if self.publication_date else None
        }


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }
