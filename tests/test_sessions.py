class TestRead:
    async def test_read_root(self, async_client):
        response = await async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "API is running."}

    async def test_read_bad_session(self, async_client):
        """
        Get a session by code that does not exist.
        """
        response = await async_client.get("/sessions/123")
        assert response.status_code == 404
