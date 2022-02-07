from flask import Blueprint, render_template


def construct_user_page(users: dict) -> Blueprint:
    """
    Constructs the user page blueprint.
    :param users: The users dictionary.
    :return: The user page blueprint.
    """
    user_page = Blueprint("user", __name__)

    @user_page.route("/users")
    def render_user_page() -> str:
        """
        Render the user page.
        """
        users_str = "<br>".join(users.values())
        return "<h1>Users:</h1><br>{}".format(users_str)

    return user_page
