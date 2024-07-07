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

    async def test_read_include_venues(self, async_client: AsyncClient, synthetic_venues):
        sample_venues = random.sample(synthetic_venues, 10)
        sample_ids = [venue["id"] for venue in sample_venues]
        body = {
            "include_ids": sample_ids
        }
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        result_ids = [venue["id"] for venue in venues]
        assert all(sample_id in result_ids for sample_id in sample_ids)

    async def test_read_exclude_include_venues(self, async_client: AsyncClient, synthetic_venues):
        sample_venues = random.sample(synthetic_venues, 10)
        include_sample_ids = [venue["id"] for venue in sample_venues[5:]]
        exclude_sample_ids = [venue["id"] for venue in sample_venues[:5]]

        body = {
            "include_ids": include_sample_ids,
            "exclude_ids": exclude_sample_ids
        }
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        result_ids = [venue["id"] for venue in venues]

        # Validate inclusions
        assert all(include_id in result_ids for include_id in include_sample_ids)
        # Validate exclusions
        assert all(result_id not in exclude_sample_ids for result_id in result_ids)
        

    async def test_read_conflicting_ids_venues(self, async_client: AsyncClient, synthetic_venues):
        sample_venue = synthetic_venues[0]
        body = {
            "include_ids": [sample_venue["id"]],
            "exclude_ids": [sample_venue["id"]]
        }

        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 400
