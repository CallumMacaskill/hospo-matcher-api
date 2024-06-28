import random

class TestRead:
    async def test_read_root(self, async_client):
        response = await async_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "API is running."}

    async def test_read_valid_session(self, async_client, synthetic_sessions):
        """
        Read a valid session.
        """
        sample_session = random.choice(synthetic_sessions)
        response = await async_client.get(f"/sessions/{sample_session['code']}")
        assert response.status_code == 200
        response_session = response.json()
        assert response_session == sample_session

    async def test_read_bad_session(self, async_client):
        """
        Read a session that does not exist.
        """
        response = await async_client.get("/sessions/123")
        assert response.status_code == 404
