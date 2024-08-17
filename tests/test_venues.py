import random

from bson import ObjectId
from httpx import AsyncClient


class TestRead:
    endpoint = "/venues/sample"

    async def test_read_valid_venues(self, async_client: AsyncClient, synthetic_venues):
        """
        Read a sample of venues.
        """
        response = await async_client.post(self.endpoint, json={})
        venues = response.json()
        assert response.status_code == 200
        assert len(response.json()) == 10
        assert all(venue in synthetic_venues for venue in venues)

    async def test_read_exclude_venues(
        self, async_client: AsyncClient, synthetic_venues
    ):
        """
        Read venues and apply exclusions.
        """
        sample_venues = random.sample(synthetic_venues, 10)
        sample_ids = [venue["id"] for venue in sample_venues]
        body = {"exclude_ids": sample_ids}
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        assert all(venue["id"] not in sample_venues for venue in venues)

    async def test_read_include_venues(
        self, async_client: AsyncClient, synthetic_venues
    ):
        """
        Read venues and apply inclusions.
        """
        sample_venues = random.sample(synthetic_venues, 10)
        sample_ids = [venue["id"] for venue in sample_venues]
        body = {"include_ids": sample_ids}
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        result_ids = [venue["id"] for venue in venues]
        assert all(sample_id in result_ids for sample_id in sample_ids)

    async def test_read_exclude_include_venues(
        self, async_client: AsyncClient, synthetic_venues
    ):
        """
        Read venues and apply exclusions and inclusions.
        """
        sample_venues = random.sample(synthetic_venues, 10)
        include_sample_ids = [venue["id"] for venue in sample_venues[5:]]
        exclude_sample_ids = [venue["id"] for venue in sample_venues[:5]]

        body = {"include_ids": include_sample_ids, "exclude_ids": exclude_sample_ids}
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 200
        venues = response.json()
        result_ids = [venue["id"] for venue in venues]

        # Validate inclusions
        assert all(include_id in result_ids for include_id in include_sample_ids)
        # Validate exclusions
        assert all(result_id not in exclude_sample_ids for result_id in result_ids)

    async def test_read_conflicting_ids_venues(
        self, async_client: AsyncClient, synthetic_venues
    ):
        """
        Attempt to include and exclude the same venue.
        """
        sample_venue = synthetic_venues[0]
        body = {
            "include_ids": [sample_venue["id"]],
            "exclude_ids": [sample_venue["id"]],
        }

        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 400

    async def test_read_invalid_bson_id(self, async_client: AsyncClient):
        """
        Attempt to include and exclude non-existent venues.
        """
        body = {
            "exclude_ids": ["abc"],
        }
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 400
        response_message = response.json()
        assert response_message["detail"] == "ID is not a valid BSON ObjectId - 'abc'"

    async def test_read_invalid_ids(self, async_client: AsyncClient):
        """
        Attempt to include and exclude non-existent venues.
        """
        body = {
            "include_ids": ["000000000000000000000000"],
            "exclude_ids": ["111111111111111111111111"],
        }
        response = await async_client.post(self.endpoint, json=body)
        result_venues = response.json()
        assert response.status_code == 200
        assert len(result_venues) == 10


class TestCreate:
    endpoint = "venues/create"

    async def test_create_valid(self, async_client: AsyncClient):
        """
        Create a venue with valid attributes.
        """
        body = {
            "name": "Valid Venue",
            "region": "NZ-AUK",
            "hour_open": 10,
            "hour_closed": 22,
        }
        response = await async_client.post(self.endpoint, json=body)
        result = response.json()
        assert ObjectId(result)

    async def test_create_invalid_empty(self, async_client: AsyncClient):
        """
        Create a venue with an invalid, empty body.
        """
        response = await async_client.post(self.endpoint, json={})
        assert response.status_code == 422

    async def test_create_invalid_hours(self, async_client: AsyncClient):
        """
        Attempt to create a venue that violates the hours restriction.
        """
        body = {
            "name": "Invalid Venue Hours",
            "region": "NZ-AUK",
            "hour_open": 0,
            "hour_closed": 25,
        }
        response = await async_client.post(self.endpoint, json=body)
        assert response.status_code == 422

    async def test_create_invalid_duplicate(
        self, async_client: AsyncClient, synthetic_venues
    ):
        """
        Attempt to create a venue that is identical to another.
        """
        sample_venue = synthetic_venues[0].copy()
        del sample_venue["id"]
        response = await async_client.post(self.endpoint, json=sample_venue)
        assert response.status_code == 400
