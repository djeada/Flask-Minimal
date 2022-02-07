from typing import Union
from flask import Flask, render_template, request

from src.pages.handle_login import handle_login
from src.pages.index_page import index_page
from src.pages.user_page import construct_user_page


if __name__ == "__main__":

    app = Flask(__name__)

    users = {"admin": "James Bond", "user": "Agent Smith"}

    # create all the pages
    pages = [
        index_page,
        handle_login,
        construct_user_page(users),
    ]

    for page in pages:
        app.register_blueprint(page)

    # Run the Flask development server i.e. debug mode is on.
    # This will allow you to make changes to the code and see the changes immediately.
    app.run()
