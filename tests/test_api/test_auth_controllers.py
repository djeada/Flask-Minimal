from typing import Any

from src.storage.global_storage import add_user_to_library


def test_handle_login_post_successful(client: Any) -> None:
    user = {"name": "john", "email": "admin@admin.com", "password": "pass"}
    add_user_to_library(user)
    response = client.post(
        "/login", data=dict(username="john", password="pass"), follow_redirects=True
    )
    assert b"john" in response.data


def test_handle_login_post_invalid_username(client: Any) -> None:
    response = client.post(
        "/login", data=dict(username="invalid", password="pass"), follow_redirects=True
    )
    assert b"Invalid credentials" in response.data


def test_handle_login_post_invalid_password(client: Any) -> None:
    response = client.post(
        "/login", data=dict(username="john", password="wrong"), follow_redirects=True
    )
    assert b"Invalid credentials" in response.data
