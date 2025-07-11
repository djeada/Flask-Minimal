"""
Service layer for book management.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import or_

from src.exceptions import ConflictError, NotFoundError, ValidationError
from src.extensions import db
from src.models import Book, BookLoan, User


class BookService:
    """Service class for book-related operations."""

    @staticmethod
    def create_book(data: Dict[str, Any]) -> Book:
        """Create a new book."""
        # Validate required fields
        required_fields = ["title", "author"]
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"{field} is required")

        # Check if book with same ISBN already exists
        if data.get("isbn"):
            existing_book = Book.query.filter_by(isbn=data["isbn"]).first()
            if existing_book:
                raise ConflictError("Book with this ISBN already exists")

        book = Book.from_dict(data)
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_book_by_id(book_id: int) -> Optional[Book]:
        """Get book by ID."""
        book = Book.query.get(book_id)
        if not isinstance(book, Book):
            return None
        return book

    @staticmethod
    def get_all_books(
        page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated list of all books with optional search."""
        query = Book.query

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Book.title.ilike(search_term),
                    Book.author.ilike(search_term),
                    Book.isbn.ilike(search_term),
                )
            )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "books": [book.to_dict() for book in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "search": search,
        }

    @staticmethod
    def update_book(book_id: int, data: Dict[str, Any]) -> Book:
        """Update book information."""
        book = BookService.get_book_by_id(book_id)
        if not book:
            raise NotFoundError("Book not found")

        # Update allowed fields
        allowed_fields = [
            "title",
            "author",
            "isbn",
            "year",
            "description",
            "total_copies",
        ]
        for field in allowed_fields:
            if field in data:
                setattr(book, field, data[field])

        # Update available copies if total copies changed
        if "total_copies" in data:
            borrowed_count = BookLoan.query.filter_by(
                book_id=book_id, is_returned=False
            ).count()
            book.available_copies = max(0, book.total_copies - borrowed_count)

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id: int) -> bool:
        """Delete book if no active loans exist."""
        book = BookService.get_book_by_id(book_id)
        if not book:
            raise NotFoundError("Book not found")

        # Check for active loans
        active_loans = BookLoan.query.filter_by(
            book_id=book_id, is_returned=False
        ).count()

        if active_loans > 0:
            raise ConflictError("Cannot delete book with active loans")

        db.session.delete(book)
        db.session.commit()
        return True

    @staticmethod
    def borrow_book(book_id: int, user_id: int, days: int = 14) -> BookLoan:
        """Borrow a book."""
        book = BookService.get_book_by_id(book_id)
        if not book:
            raise NotFoundError("Book not found")

        if book.available_copies <= 0:
            raise ConflictError("Book is not available for borrowing")

        user = User.query.get(user_id)
        if not user or not user.is_active:
            raise NotFoundError("User not found or inactive")

        # Check if user already has this book borrowed
        existing_loan = BookLoan.query.filter_by(
            book_id=book_id, user_id=user_id, is_returned=False
        ).first()

        if existing_loan:
            raise ConflictError("User already has this book borrowed")

        # Create loan
        loan = BookLoan(
            book_id=book_id,
            user_id=user_id,
            due_date=datetime.utcnow() + timedelta(days=days),
        )

        # Update book availability
        book.available_copies -= 1
        book.is_available = book.available_copies > 0

        db.session.add(loan)
        db.session.commit()

        if not isinstance(loan, BookLoan):
            raise RuntimeError("Failed to create loan")
        return loan

    @staticmethod
    def return_book(loan_id: int) -> BookLoan:
        """Return a borrowed book."""
        loan = BookLoan.query.get(loan_id)
        if not isinstance(loan, BookLoan):
            raise NotFoundError("Loan not found")

        if loan.is_returned:
            raise ConflictError("Book already returned")

        # Mark as returned
        loan.is_returned = True
        loan.returned_at = datetime.utcnow()

        # Update book availability
        book = loan.book
        if hasattr(book, "available_copies") and hasattr(book, "is_available"):
            book.available_copies += 1  # type: ignore[attr-defined]
            book.is_available = True  # type: ignore[attr-defined]
        db.session.commit()
        return loan

    @staticmethod
    def get_user_loans(user_id: int, active_only: bool = False) -> List[BookLoan]:
        """Get all loans for a user."""
        query = BookLoan.query.filter_by(user_id=user_id)

        if active_only:
            query = query.filter_by(is_returned=False)

        loans = query.all()
        if not isinstance(loans, list):
            return []
        return loans

    @staticmethod
    def get_overdue_loans() -> List[BookLoan]:
        """Get all overdue loans."""
        loans = BookLoan.query.filter(
            BookLoan.is_returned.is_(False), BookLoan.due_date < datetime.utcnow()
        ).all()
        if not isinstance(loans, list):
            return []
        return loans
