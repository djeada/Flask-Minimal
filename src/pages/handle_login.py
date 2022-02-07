from flask import Blueprint, render_template, request

from src.pages import user_page

handle_login = Blueprint("handle_login", __name__)

@handle_login.route("/handle_login", methods=["POST"])
def render_handle_login() -> str:
    """
    Handle a login request.
    :return: String with the result of the login.
    """
    assert request.method == "POST"

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin":
        msg = "You have accessed the main server of Zion"
        return msg
    else:
        error = "Invalid credentials"
        return render_template("home.html", error=error)