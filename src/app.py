"""
This script starts a Flask application that allows users to interact with a
library. The application allows users to view, borrow and return books, as well
 as add new books and users to the library. The application uses a global
 storage object to store the books and users.

The script defines a function `fill_with_dummy_data` that fills the global
storage object with some dummy data for testing purposes.

The script also defines a function `main` that creates an instance of the
`LibraryApp` class and runs the Flask development server in debug mode. Debug
mode allows changes to be made to the code and seen immediately.

To start the application, run this script directly by executing the command
`python app.py` in the terminal.
"""

from src.library_app.library_app import LibraryApp
from src.storage.global_storage import add_book_to_library, add_user_to_library

DEBUG = True


def fill_with_dummy_data() -> None:
    """
    Fill the global storage with dummy data for testing purposes.
    """
    # Those are just some dummy data to test the application
    # In a real life scenario, you would probably have a database
    users = [
        {"name": "admin", "email": "admin@admin.com", "password": "admin"},
        {
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
        {"name": "Bob", "email": "bob@example.com", "password": "password456"},
        {
            "name": "Charlie",
            "email": "charlie@example.com",
            "password": "password789",
        },
    ]
    books = [
        {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "year": 1954,
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "year": 1937,
        },
        {
            "title": "The Silmarillion",
            "author": "J.R.R. Tolkien",
            "year": 1977,
        },
        {
            "title": "The Fellowship of the Ring",
            "author": "J.R.R. Tolkien",
            "year": 1954,
        },
        {
            "title": "The Two Towers",
            "author": "J.R.R. Tolkien",
            "year": 1954,
        },
        {
            "title": "The Return of the King",
            "author": "J.R.R. Tolkien",
            "year": 1955,
        },
    ]

    for user in users:
        add_user_to_library(user)

    for book in books:
        add_book_to_library(book)


def main() -> None:
    """
    The main function."""

    if DEBUG:
        fill_with_dummy_data()

    app = LibraryApp()

    # Run the Flask development server i.e. debug mode is on.
    # This will allow you to make changes to the code and see
    # the changes immediately.
    app.run()


if __name__ == "__main__":
    main()
