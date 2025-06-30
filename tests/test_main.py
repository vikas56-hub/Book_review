from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book():
    res = client.post("/books", json={"title": "Test Book", "author": "Author"})
    assert res.status_code == 200
    assert res.json()["title"] == "Test Book"

def test_get_books():
    res = client.get("/books")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_add_review_and_get():
    res = client.post("/books", json={"title": "With Review", "author": "Author"})
    book_id = res.json()["id"]
    client.post(f"/books/{book_id}/reviews", json={"content": "Nice!", "rating": 5})
    res2 = client.get(f"/books/{book_id}/reviews")
    assert res2.status_code == 200
    assert len(res2.json()) >= 1
