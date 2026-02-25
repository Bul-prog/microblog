from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ALICE = {"api-key": "alice-key"}


def test_create_tweet():
    payload = {"tweet_data": "Hello world!", "tweet_media_ids": None}
    r = client.post("/api/tweets", headers=ALICE, json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["result"] is True
    assert isinstance(body["tweet_id"], int)


def test_get_feed():
    r = client.get("/api/tweets", headers=ALICE)
    assert r.status_code == 200
    body = r.json()
    assert body["result"] is True
    assert isinstance(body["tweets"], list)

    if body["tweets"]:
        t0 = body["tweets"][0]
        assert "id" in t0
        assert "content" in t0
        assert "attachments" in t0
        assert "author" in t0
        assert "likes" in t0
