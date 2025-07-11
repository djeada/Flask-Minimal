from typing import Any


def test_index_page(client: Any) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Welcome to Library</title>" in response.data
