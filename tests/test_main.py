import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_memo_crud():
    create_resp = client.post(
        "/memos", json={"title": "test", "content": "hello"}
    )
    assert create_resp.status_code == 201
    created = create_resp.json()

    memo_id = created["id"]

    get_resp = client.get(f"/memos/{memo_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "test"

    update_resp = client.put(
        f"/memos/{memo_id}", json={"title": "updated", "content": "changed"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "updated"

    list_resp = client.get("/memos")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    delete_resp = client.delete(f"/memos/{memo_id}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/memos/{memo_id}")
    assert missing_resp.status_code == 404
