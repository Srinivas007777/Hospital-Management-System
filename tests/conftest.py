
import pytest
from fastapi.testclient import TestClient

from main import app
from database import get_connection


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    # Register the test user if it does not already exist
    client.post("/auth/register", json={
        "username": "pytestuser",
        "email": "pytestuser@example.com",
        "password": "Test@12345"
    })

    # Give the test account Admin permissions
    conn = get_connection()
    conn.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        ("Admin", "pytestuser")
    )
    conn.commit()
    conn.close()

    # Log in after assigning the role
    response = client.post("/auth/login", data={
        "username": "pytestuser",
        "password": "Test@12345"
    })

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
