import random

from httpx import AsyncClient


class TestRead:
    async def test_read_valid_session(self, async_client, synthetic_sessions):
        """
        Read a session.
        """
        sample_session = random.choice(synthetic_sessions)
        response = await async_client.get(f"/sessions/{sample_session['code']}")
        assert response.status_code == 200
        response_session = response.json()
        assert response_session == sample_session

    async def test_read_invalid_session(self, async_client):
        """
        Attempt to read a non-existent session.
        """
        response = await async_client.get("/sessions/123")
        assert response.status_code == 404


class TestCreate:
    async def test_create_valid_session(self, async_client: AsyncClient):
        """
        Create a session with valid attributes.
        """
        body = {
            "code": "valid_code",
            "location": "NZ-AUK",
        }
        response = await async_client.post("/sessions/", json=body)
        assert response.status_code == 200

    async def test_create_invalid_duplicate_code(
        self, async_client: AsyncClient, synthetic_sessions
    ):
        """
        Attempt to create a session with the same code as another session.
        """
        sample_venue = synthetic_sessions[0].copy()
        body = {"code": sample_venue["code"], "location": sample_venue["location"]}
        response = await async_client.post("/sessions/", json=body)
        assert response.status_code == 400


class TestVotes:
    async def test_valid_votes(
        self, async_client: AsyncClient, synthetic_sessions, synthetic_venues
    ):
        """
        Submit user votes for new venue IDs.
        """
        # Get sample session and user id
        session = synthetic_sessions[0]
        user_ids = list(session["user_votes"].keys())
        user_id = user_ids[0]

        # Get sample venues for votes
        venue_ids = {venue["id"] for venue in synthetic_venues}
        user_votes = session["user_votes"][user_id]
        venue_id_difference = list(venue_ids - set(user_votes))
        venue_id_votes = random.sample(venue_id_difference, 5)

        # Submit votes
        body = {"upvotes": venue_id_votes}
        response = await async_client.post(
            f"/sessions/{session['code']}/{user_id}", json=body
        )
        assert response.status_code == 200
        assert response.json() == session["id"]

        # Validate votes are applied
        response = await async_client.get(f"/sessions/{session['code']}")
        assert response.status_code == 200
        updated_session = response.json()
        local_votes = user_votes + venue_id_votes
        db_votes = updated_session["user_votes"][user_id]
        assert local_votes.sort() == db_votes.sort()

    async def test_invalid_code(self, async_client: AsyncClient):
        """
        Attempt to submit votes on a non-existent session.
        """
        body = {"upvotes": []}
        response = await async_client.post(f"/sessions/abc/user_abc", json=body)
        assert response.status_code == 404
        assert response.json() == {"detail": "Session with code abc not found."}

    async def test_invalid_venue_ids(
        self, async_client: AsyncClient, synthetic_sessions
    ):
        """
        Attempt to vote for non-existent venues.
        """
        session = synthetic_sessions[0]
        venue_ids = ["000000000000000000000000", "111111111111111111111111"]
        body = {"upvotes": venue_ids}
        response = await async_client.post(
            f"/sessions/{session['code']}/user_abc", json=body
        )

        # Validate response
        assert response.status_code == 404
        response_message = response.json()
        assert str.startswith(response_message["detail"], "Venues with IDs not found: ")
        for id in venue_ids:
            assert id in response_message["detail"]

    async def test_invalid_bson_ids(
        self, async_client: AsyncClient, synthetic_sessions
    ):
        """
        Attempt to vote for venues with bad IDs.
        """
        session = synthetic_sessions[0]
        venue_ids = ["abc"]
        body = {"upvotes": venue_ids}
        response = await async_client.post(
            f"/sessions/{session['code']}/user_abc", json=body
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "ID is not a valid BSON ObjectId - 'abc'"}
