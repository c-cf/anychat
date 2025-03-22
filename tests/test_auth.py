import pytest
from fastapi.testclient import TestClient
from main import app
from services.permission_service import PermissionService
from services.auth_service import get_current_user, User

client = TestClient(app)

# Mock the get_current_user dependency
def mock_get_current_user():
    return User(id="test_user", username="testuser", email="testuser@example.com")

# Override the dependency
app.dependency_overrides[get_current_user] = mock_get_current_user

# Mock the PermissionService
class MockPermissionService(PermissionService):
    def check_permission(self, user_id: str, permission: str) -> bool:
        return True  # Always return True for testing purposes

# Override the dependency
app.dependency_overrides[PermissionService] = MockPermissionService

def test_assign_role():
    response = client.post("/roles/test_user", json={"role": "admin"})
    assert response.status_code == 200
    assert response.json() == {"message": "Role assigned successfully"}

def test_add_role():
    response = client.post("/roles", json={"role": "new_role", "permissions": ["add_document"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Role added successfully"}

def test_email_verification():
    # 模擬註冊
    response = client.post("/register", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "Please verify your email" in response.json()["message"]

    # 模擬驗證
    verification_token = "mock_verification_token"  # 使用測試時生成的 Token
    response = client.get(f"/verify-email?token={verification_token}")
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully"}