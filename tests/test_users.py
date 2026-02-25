from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ALICE = {"api-key": "alice-key"}
BOB = {"api-key": "bob-key"}


def test_get_me_ok():
    r = client.get("/api/users/me", headers=ALICE)
    assert r.status_code == 200
    body = r.json()
    assert body["result"] is True
    assert body["user"]["name"] == "alice"
    assert isinstance(body["user"]["followers"], list)
    assert isinstance(body["user"]["following"], list)


def test_get_me_unauthorized():
    r = client.get("/api/users/me", headers={"api-key": "wrong"})
    assert r.status_code in (401, 422)


def test_follow_unfollow_cycle():
    r1 = client.post("/api/users/2/follow", headers=ALICE)
    assert r1.status_code == 200
    assert r1.json()["result"] is True

    r2 = client.get("/api/users/me", headers=ALICE)
    assert r2.status_code == 200
    following_ids = [u["id"] for u in r2.json()["user"]["following"]]
    assert 2 in following_ids

    r3 = client.delete("/api/users/2/follow", headers=ALICE)
    assert r3.status_code == 200
    assert r3.json()["result"] is True

    r4 = client.get("/api/users/me", headers=ALICE)
    following_ids2 = [u["id"] for u in r4.json()["user"]["following"]]
    assert 2 not in following_ids2
