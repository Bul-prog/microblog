from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ALICE = {"api-key": "alice-key"}


def test_upload_media():
    files = {
        "file": ("test.png", b"fake-image-bytes", "image/png")
    }
    r = client.post("/api/medias", headers=ALICE, files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["result"] is True
    assert isinstance(body["media_id"], int)
