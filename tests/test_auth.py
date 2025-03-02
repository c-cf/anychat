import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_assign_role():
    response = client.post("/roles/test_user", json={"role": "admin"})
    assert response.status_code == 200
    assert response.json() == {"message": "Role assigned successfully"}

def test_add_role():
    response = client.post("/roles", json={"role": "new_role", "permissions": ["add_document"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Role added successfully"}