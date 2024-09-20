import pytest
from fastapi.testclient import TestClient
from main import app
from src.book_schemas.input import BookCreate
from sqlalchemy.orm import Session
from src.database import get_db
from unittest.mock import MagicMock

client = TestClient(app)


@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    yield db


@pytest.mark.parametrize(
    "book_data, expected_status_code, expected_message",
    [
        ({"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publication_date": "1925-04-10"}, 200, "Success"),
        ({"title": "", "author": "Author", "publication_date": "1925-04-10"}, 422, "Validation Error"),
        ({"title": "Valid Title", "author": "", "publication_date": "invalid-date"}, 422, "Validation Error"),
    ],
)
def test_create_book(book_data, expected_status_code, expected_message, mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post("/books/", json=book_data)

    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.json()["title"] == book_data["title"]
        assert response.json()["author"] == book_data["author"]
    else:
        assert expected_message in response.text


@pytest.mark.parametrize(
    "book_id, db_book, expected_status_code",
    [
        (1, {"id": 1, "title": "1984", "author": "George Orwell", "publication_date": "1949-06-08"}, 200),
        (999, None, 404),
    ],
)
def test_get_book(book_id, db_book, expected_status_code, mock_db):
    mock_db.get_by_id.return_value = db_book
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.get(f"/books/{book_id}")
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.json()["title"] == db_book["title"]
        assert response.json()["author"] == db_book["author"]
    else:
        assert "Книга не найдена" in response.text


@pytest.mark.parametrize(
    "book_id, db_exists, expected_status_code",
    [
        (1, True, 200),
        (999, False, 404),
    ],
)
def test_delete_book(book_id, db_exists, expected_status_code, mock_db):
    mock_db.delete.return_value = db_exists
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == expected_status_code
    if expected_status_code == 200:
        assert response.json()["message"] == "Книга успешно удалена"
    else:
        assert "Книга не найдена" in response.text
