from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users?skip=0&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id():
    response = client.get("/user/1")
    assert response.status_code in [200, 404]

def test_random_user():
    response = client.get("/random")
    assert response.status_code == 200
