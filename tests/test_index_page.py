import pytest
from src.app import create_app


@pytest.fixture
def app():
    """
    Create the Flask application.
    :return: The Flask application.
    """
    return create_app()


def test_index_page(client):
    """
    Test the index page.
    :param client: The Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert b'<link rel="stylesheet" href="../../static/css/main.css">' in response.data
    assert b"<h1>Welcome to my home page!</h1>" in response.data
    assert (
        b'<p>Check the user <a href="/users">page</a> to see if you are logged in.</p>'
        in response.data
    )
