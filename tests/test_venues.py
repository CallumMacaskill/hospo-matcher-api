from hospo_matcher.utils.logger import log


async def test_read_venues(async_client):
    response = await async_client.get("/venues/")
    assert response.status_code == 200
    assert len(response.json()) == 10
