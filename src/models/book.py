"""
This module defines the Book data class which represents a book in the library.
"""

from dataclasses import dataclass


@dataclass
class Book:
    """
    A data class that represents a book in the library.

    :ivar id: The unique identifier of the book.
    :ivar title: The title of the book.
    :ivar author: The author of the book.
    :ivar year: The year the book was published.
    """

    id: int
    title: str
    author: str
    year: int

    @classmethod
    def from_dict(cls, book_dict: dict) -> "Book":
        """
        Creates a new Book instance from a dictionary.
        """
        return cls(
            id=int(book_dict["id"]),
            title=str(book_dict["title"]),
            author=str(book_dict["author"]),
            year=int(book_dict["year"]),
        )
