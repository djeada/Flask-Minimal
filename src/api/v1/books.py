"""
Books API endpoints.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import Schema, fields

from src.api.decorators import admin_required, validate_json
from src.exceptions import ValidationError as ServiceValidationError
from src.services.book_service import BookService

books_bp = Blueprint("books", __name__)


class BookCreateSchema(Schema):
    """Schema for book creation validation."""

    title = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    author = fields.Str(required=True, validate=lambda x: len(x) >= 1)
    isbn = fields.Str(validate=lambda x: len(x) in [10, 13])
    year = fields.Int(validate=lambda x: 1000 <= x <= 2100)
    description = fields.Str()
    total_copies = fields.Int(validate=lambda x: x >= 1, load_default=1)


class BookUpdateSchema(Schema):
    """Schema for book update validation."""

    title = fields.Str(validate=lambda x: len(x) >= 1)
    author = fields.Str(validate=lambda x: len(x) >= 1)
    isbn = fields.Str(validate=lambda x: len(x) in [10, 13])
    year = fields.Int(validate=lambda x: 1000 <= x <= 2100)
    description = fields.Str()
    total_copies = fields.Int(validate=lambda x: x >= 1)


class BorrowBookSchema(Schema):
    """Schema for book borrowing validation."""

    days = fields.Int(validate=lambda x: 1 <= x <= 90, load_default=14)


@books_bp.route("", methods=["GET"])
def get_books():
    """Get paginated list of all books with optional search."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        search = request.args.get("search", "")

        result = BookService.get_all_books(
            page=page, per_page=per_page, search=search if search else None
        )
        return jsonify(result), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve books"}), 500


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get book by ID."""
    try:
        book = BookService.get_book_by_id(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({"book": book.to_dict()}), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve book"}), 500


@books_bp.route("", methods=["POST"])
@jwt_required()
@admin_required
@validate_json(BookCreateSchema)
def create_book():
    """Create a new book (admin only)."""
    try:
        data = request.get_json()
        book = BookService.create_book(data)

        return (
            jsonify({"message": "Book created successfully", "book": book.to_dict()}),
            201,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to create book"}), 500


@books_bp.route("/<int:book_id>", methods=["PUT"])
@jwt_required()
@admin_required
@validate_json(BookUpdateSchema)
def update_book(book_id):
    """Update book information (admin only)."""
    try:
        data = request.get_json()
        book = BookService.update_book(book_id, data)

        return (
            jsonify({"message": "Book updated successfully", "book": book.to_dict()}),
            200,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to update book"}), 500


@books_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_book(book_id):
    """Delete book (admin only)."""
    try:
        BookService.delete_book(book_id)
        return jsonify({"message": "Book deleted successfully"}), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to delete book"}), 500


@books_bp.route("/<int:book_id>/borrow", methods=["POST"])
@jwt_required()
@validate_json(BorrowBookSchema)
def borrow_book(book_id):
    """Borrow a book."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        days = data.get("days", 14)

        loan = BookService.borrow_book(book_id, user_id, days)

        return (
            jsonify({"message": "Book borrowed successfully", "loan": loan.to_dict()}),
            201,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to borrow book"}), 500


@books_bp.route("/loans/<int:loan_id>/return", methods=["POST"])
@jwt_required()
def return_book(loan_id):
    """Return a borrowed book."""
    try:
        user_id = get_jwt_identity()
        user_role = get_jwt().get("role", "user")

        # Get loan to check ownership
        from src.models import BookLoan

        loan = BookLoan.query.get(loan_id)
        if not loan:
            return jsonify({"error": "Loan not found"}), 404

        # Check if user owns the loan or is admin
        if loan.user_id != user_id and user_role != "admin":
            return jsonify({"error": "Access denied"}), 403

        loan = BookService.return_book(loan_id)

        return (
            jsonify({"message": "Book returned successfully", "loan": loan.to_dict()}),
            200,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to return book"}), 500


@books_bp.route("/loans/overdue", methods=["GET"])
@jwt_required()
@admin_required
def get_overdue_loans():
    """Get all overdue loans (admin only)."""
    try:
        loans = BookService.get_overdue_loans()

        return (
            jsonify(
                {
                    "overdue_loans": [loan.to_dict() for loan in loans],
                    "total": len(loans),
                }
            ),
            200,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve overdue loans"}), 500
