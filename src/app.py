from typing import Union
from flask import Flask, render_template, request

app = Flask(__name__)

users = {"admin": "James Bond", "user": "Agent Smith"}


@app.route("/")
def hello() -> str:
    """
    Return a friendly HTTP greeting.
    :return: String representing the HTTP response.
    """
    return "Hello World!"


@app.route("/user")
def show_user_overview() -> str:
    """
    Show a list of all users. This will be served as an HTML page.
    :return: String with user overview.
    """
    users_str = "<br>".join(users.values())
    return "<h1>Users:</h1><br>{}".format(users_str)


@app.route("/user/<username>")
def show_user_profile(username: str) -> str:
    """
    Show the profile of a specific user. This will be served as an HTML page.
    :param username: The username of the user to show the profile of.
    :return: String with user profile.
    """
    return "User {}".format(username)


@app.route("/pots/")
@app.route("/post/<name>")
def post(name: Union[str, None]=None) -> str:
    """
    Show a post. This will be served as an HTML page.
    :param name: The name of the post to show.
    :return: String with post.
    """
    return render_template("post.html", name=name)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/handle_login", methods=["POST"])
def handle_login() -> str:
    """
    Handle a login request.
    :return: String with the result of the login.
    """
    assert request.method == "POST"

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin":
        return "You have accesed the main server of Zion"
    else:
        error = "Invalid credentials"
        return render_template("login.html", error=error)


if __name__ == "__main__":
    # Run the Flask development server i.e. debug mode is on. 
    # This will allow you to make changes to the code and see the changes immediately.
    app.run()
