def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running."}


def test_read_sessions(client):
    response = client.get("/sessions/123")
    assert response.status_code == 404
