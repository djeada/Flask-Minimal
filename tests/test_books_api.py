import pytest
from src.app import create_app

books = [
    {
        "id": 1,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "year": 1954,
    },
    {"id": 2, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
    {
        "id": 3,
        "title": "The Silmarillion",
        "author": "J.R.R. Tolkien",
        "year": 1977,
    },
    {
        "id": 4,
        "title": "The Fellowship of the Ring",
        "author": "J.R.R. Tolkien",
        "year": 1954,
    },
    {
        "id": 5,
        "title": "The Two Towers",
        "author": "J.R.R. Tolkien",
        "year": 1954,
    },
    {
        "id": 6,
        "title": "The Return of the King",
        "author": "J.R.R. Tolkien",
        "year": 1955,
    },
]


@pytest.fixture
def app():
    app = create_app(books=books)
    return app


def test_get_book_api(app):
    """
    Test the get book API.
    """
    with app.test_client() as client:
        for book in books:
            response = client.get(f"/api/v1.0/books/{book['id']}")
            assert response.status_code == 200
            assert response.json == book

    response = client.get("/api/v1.0/books/7")
    assert response.status_code == 404
    assert response.json == {"error": "Book not found"}


def test_create_book_api(app):
    """
    Test the create book API.
    """
    with app.test_client() as client:
        response = client.post(
            "/api/v1.0/books",
            json={
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "year": 1937,
            },
        )
        assert response.status_code == 201
        assert response.json == {
            "id": 7,
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "year": 1937,
        }

        response = client.post(
            "/api/v1.0/books", json={"wrong_dict_key": "some_data"}
        )
        assert response.status_code == 400
        assert response.json == {"error": "Invalid book data"}
