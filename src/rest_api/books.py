from typing import List, Tuple

from flask import jsonify, Blueprint, request


def construct_books_api(books: List[dict]) -> Blueprint:
    """
    Constructs the books API blueprint.
    :param books: List of books dictionaries.
    :return: The books API blueprint.
    """
    books_api = Blueprint("books_api", __name__)

    @books_api.route("/api/v1.0/books/<int:book_id>")
    def get_book(book_id: int) -> Tuple[str, int]:
        """
        Get a book by its ID.
        """
        for book in books:
            if book["id"] == book_id:
                return jsonify(book), 200

        return jsonify({"error": "Book not found"}), 404

    @books_api.route("/api/v1.0/books", methods=["POST"])
    def create_book() -> Tuple[str, int]:
        """
        Create a new book.
        """
        book_keys = books[0].keys()

        if not request.json or len([True for key in book_keys if key in request.json]) == 0:
            return jsonify({"error": "Invalid book data"}), 400
        
        book = { "id": len(books) + 1, "title": request.json["title"], "author": request.json["author"], "year": request.json["year"] }
        books.append(book)
        return jsonify(book), 201

    return books_api


