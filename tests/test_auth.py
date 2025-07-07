import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

USER_DATA = {
    "email": "loginuser@email.com",
    "full_name": "Login User",
    "password": "senha12345",
}


def test_login_success():
    client.post("/api/v1/user/", json=USER_DATA)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": USER_DATA["email"], "password": USER_DATA["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": USER_DATA["email"], "password": "senha_errada"},
    )
    assert response.status_code == 401
    assert "E-mail ou senha incorretos" in response.text
