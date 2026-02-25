from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck_root():
    r = client.get("/")
    assert r.status_code == 200


def test_swagger_available():
    r = client.get("/docs")
    assert r.status_code == 200
