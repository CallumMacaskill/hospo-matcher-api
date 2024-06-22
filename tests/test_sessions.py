async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running."}

async def test_read_sessions(async_client):
    response = await async_client.get("/sessions/123")
    assert response.status_code == 404
