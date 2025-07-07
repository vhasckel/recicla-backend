import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user_success():
    user_data = {
        "email": "novo@email.com",
        "full_name": "Novo Usuário",
        "password": "senha12345",
    }
    response = client.post("/api/v1/user/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

    global created_user_id
    created_user_id = data["id"]


def test_create_user_duplicate_email():
    user_data = {
        "email": "duplicado@email.com",
        "full_name": "Usuário Duplicado",
        "password": "senha12345",
    }
    # Cria o usuário pela primeira vez
    client.post("/api/v1/user/", json=user_data)
    # Tenta criar novamente
    response = client.post("/api/v1/user/", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.text


def test_get_user_by_id():
    response = client.get(f"/api/v1/user/{created_user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_user_id


def test_update_user():
    update_data = {"full_name": "User atualizado"}
    response = client.put(f"/api/v1/user/{created_user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "User atualizado"


def test_delete_user():
    response = client.delete(f"/api/v1/user/{created_user_id}")
    assert response.status_code == 200
    # Tenta buscar o usuário deletado
    response = client.get(f"/api/v1/user/{created_user_id}")
    assert response.status_code == 404
