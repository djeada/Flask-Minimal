"""
Custom exception classes for the application.
"""


class LibraryException(Exception):
    """Base exception class for library application."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(LibraryException):
    """Exception for validation errors."""

    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(LibraryException):
    """Exception for resource not found errors."""

    def __init__(self, message: str):
        super().__init__(message, 404)


class ConflictError(LibraryException):
    """Exception for conflict errors."""

    def __init__(self, message: str):
        super().__init__(message, 409)


class UnauthorizedError(LibraryException):
    """Exception for unauthorized access."""

    def __init__(self, message: str):
        super().__init__(message, 401)


class ForbiddenError(LibraryException):
    """Exception for forbidden access."""

    def __init__(self, message: str):
        super().__init__(message, 403)
