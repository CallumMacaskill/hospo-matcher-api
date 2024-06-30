import random

from httpx import AsyncClient
from bson import ObjectId

class TestRead:
    async def test_read_valid_venues(self, async_client: AsyncClient, synthetic_venues):
        response = await async_client.get("/venues/")
        venues = response.json()
        assert response.status_code == 200
        assert len(response.json()) == 10
        assert all(venue in synthetic_venues for venue in venues)

    async def test_read_exclude_venues(self, async_client: AsyncClient, synthetic_venues):
        sample_venues = random.sample(synthetic_venues, 10)
        ids = [ObjectId(venue["id"]) for venue in sample_venues]
        query = {"id": {"$in": ids}}
        response = await async_client.post("/venues/", json=query)
        assert response.status_code == 200
        venues = response.json()
        assert all(venue["id"] not in ids for venue in venues)