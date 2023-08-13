from fastapi.testclient import TestClient
from api import app
import jwt
import os

client = TestClient(app)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
payload = {"user_id": 123, "role": "test"}  # Example payload

VALID_JWT_TOKEN = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
INVALID_JWT_TOKEN = "invalid_jwt_token"

def test_get_state():
    response = client.get("/state")
    assert response.status_code == 200
    data = response.json()
    assert "power" in data
    assert "counter" in data

def test_increase_power():
    response = client.post("/power/increase")
    assert response.status_code == 200
    data = response.json()
    assert data['power'] >= 10  # Assuming a base power of 0 and increase by 10%

def test_decrease_power():
    response = client.post("/power/decrease")
    assert response.status_code == 200
    data = response.json()
    assert data['power'] <= 90  # Assuming a base power of 100% and decrease by 10%

def test_increase_counter():
    response = client.post("/counter/increase")
    assert response.status_code == 200
    data = response.json()
    assert data['counter'] >= 10  # Assuming a base counter of 0 and increase by 10s

def test_decrease_counter():
    response = client.post("/counter/decrease")
    assert response.status_code == 200
    data = response.json()
    assert data['counter'] <= 90  # Assuming a base counter of 100s and decrease by 10s

def test_cancel_operation():
    headers = {"Authorization": f"Bearer {VALID_JWT_TOKEN}"}
    response = client.post("/cancel", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['power'] == 0
    assert data['counter'] == 0

def test_invalid_cancel_operation():
    headers = {"Authorization": f"Bearer {INVALID_JWT_TOKEN}"}
    response = client.post("/cancel", headers=headers)
    assert response.status_code == 401  # Unauthorized

