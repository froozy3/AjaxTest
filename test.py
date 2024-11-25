import pytest
import requests
from starlette.testclient import TestClient

from routes import create, app
from db import SessionLocal, get_db

BASE_URL = "http://127.0.0.1:8000"
session = get_db()


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_set_status(client):
    status_data = {"status": "Test status"}
    response = client.post("/setStatus", json=status_data)

    assert response.status_code == 200
    assert response.json() == {"message": "status created successfully!"}
