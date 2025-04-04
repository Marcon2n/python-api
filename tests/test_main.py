import pytest
import sys
print(sys.path)
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import if your file structure is different

client = TestClient(app)


def test_register_user():
    # Test user registration
    response = client.post("/register", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Tạo mới thành công"
    assert len(response.json()["list"]) == 1


def test_register_existing_user():
    # Test registering a user that already exists
    client.post("/register", json={"username": "testuser", "password": "password123"})
    response = client.post("/register", json={"username": "testuser", "password": "password456"})
    assert response.status_code == 400
    assert response.json()["detail"] == "User đã tồn tại"


def test_login_success():
    # Test successful login
    client.post("/register", json={"username": "testlogin", "password": "mypassword"})
    response = client.post("/login", json={"username": "testlogin", "password": "mypassword"})
    assert response.status_code == 200
    assert response.json()["message"] == "Login thành công"


def test_login_wrong_password():
    # Test login with incorrect password
    client.post("/register", json={"username": "wrongpassword", "password": "correctpassword"})
    response = client.post("/login", json={"username": "wrongpassword", "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Mật khẩu không đúng"


def test_login_nonexistent_user():
    # Test login with a nonexistent user
    response = client.post("/login", json={"username": "nonexistent", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Tài khoản không tồn tại"


def test_get_all_users():
    # Test retrieving all users
    client.post("/register", json={"username": "user1", "password": "pass1"})
    client.post("/register", json={"username": "user2", "password": "pass2"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) >= 2
