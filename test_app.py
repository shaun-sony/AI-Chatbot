import os
from unittest.mock import MagicMock, patch

# Prevent the OpenAI client from complaining about a missing key
# when the application is imported during testing.
os.environ.setdefault("OPENAI_API_KEY", "test-api-key")

from app import app


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "Backend is running."


def test_empty_message():
    client = app.test_client()

    response = client.post("/chat", json={"message": ""})

    assert response.status_code == 400
    assert response.get_json()["reply"] == "Please type a message."


def test_message_too_long():
    client = app.test_client()

    long_message = "A" * 501

    response = client.post(
        "/chat",
        json={"message": long_message}
    )

    assert response.status_code == 400
    assert "500 characters" in response.get_json()["reply"]


def test_chat_with_mocked_openai():
    client = app.test_client()

    fake_response = MagicMock()
    fake_response.output_text = "The service desk is open from 9 AM to 5 PM."

    with patch(
        "app.client.responses.create",
        return_value=fake_response
    ):
        response = client.post(
            "/chat",
            json={"message": "What are the service desk opening hours?"}
        )

    assert response.status_code == 200
    assert response.get_json()["reply"] == (
        "The service desk is open from 9 AM to 5 PM."
    )
