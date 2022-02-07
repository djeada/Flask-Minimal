from typing import Union
from flask import Flask, render_template, request

from src.pages.handle_login import handle_login
from src.pages.index_page import index_page
from src.pages.user_page import construct_user_page
from src.rest_api.books import construct_books_api

def create_app(users=list(), books=dict()) -> Flask:
    """
    Create the Flask application.
    :return: The Flask application.
    """
    app = Flask(__name__)

    # create all the pages
    pages = [
        index_page,
        handle_login,
        construct_user_page(users),
        construct_books_api(books)
    ]

    for page in pages:
        app.register_blueprint(page)

    return app

if __name__ == "__main__":

    # Those are just some dummy data to test the application
    # In a real life scenario, you would probably have a database
    users = {"admin": "James Bond", "user": "Agent Smith"}

    books = [ {"id": 1, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "year": 1954},
                {"id": 2, "title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
                {"id": 3, "title": "The Silmarillion", "author": "J.R.R. Tolkien", "year": 1977},
                {"id": 4, "title": "The Fellowship of the Ring", "author": "J.R.R. Tolkien", "year": 1954},
                {"id": 5, "title": "The Two Towers", "author": "J.R.R. Tolkien", "year": 1954},
                {"id": 6, "title": "The Return of the King", "author": "J.R.R. Tolkien", "year": 1955},
             ]

    app = create_app(users, books)

    # Run the Flask development server i.e. debug mode is on.
    # This will allow you to make changes to the code and see the changes immediately.
    app.run()
