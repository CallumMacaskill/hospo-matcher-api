import random

from httpx import AsyncClient


class TestRead:
    async def test_read_valid_session(self, async_client, synthetic_sessions):
        """
        Read a valid session.
        """
        sample_session = random.choice(synthetic_sessions)
        response = await async_client.get(f"/sessions/{sample_session['code']}")
        assert response.status_code == 200
        response_session = response.json()
        assert response_session == sample_session

    async def test_read_invalid_session(self, async_client):
        """
        Read a session that does not exist.
        """
        response = await async_client.get("/sessions/123")
        assert response.status_code == 404


class TestCreate:
    async def test_create_valid_session(self, async_client: AsyncClient):
        body = {
            "code": "valid_code",
            "location": "NZ-AUK",
        }
        response = await async_client.post("/sessions/", json=body)
        assert response.status_code == 200

    async def test_create_invalid_duplicate_code(
        self, async_client: AsyncClient, synthetic_sessions
    ):
        sample_venue = synthetic_sessions[0].copy()
        body = {"code": sample_venue["code"], "location": sample_venue["location"]}
        response = await async_client.post("/sessions/", json=body)
        assert response.status_code == 400
