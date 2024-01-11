from fastapi.testclient import TestClient
from main.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200

