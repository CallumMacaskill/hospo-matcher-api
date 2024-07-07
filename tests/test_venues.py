import random

from httpx import AsyncClient
from bson import ObjectId

class TestRead:
    endpoint = "/venues/sample"
    async def test_read_valid_venues(self, async_client: AsyncClient, synthetic_venues):
        response = await async_client.post(self.endpoint, json={})
        venues = response.json()
        assert response.status_code == 200
        assert len(response.json()) == 10
        assert all(venue in synthetic_venues for venue in venues)

    async def test_read_exclude_venues(self, async_client: AsyncClient, synthetic_venues):
        sample_venues = random.sample(synthetic_venues, 10)
        sample_ids = [venue["id"] for venue in sample_venues]
        body = {
            "exclude_ids": sample_ids
        }
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        assert all(venue["id"] not in sample_venues for venue in venues)
