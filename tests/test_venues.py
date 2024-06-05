def test_read_sessions(client):
    response = client.get("/venues/")
    assert response.status_code == 200
    assert len(response.json()) == 10
