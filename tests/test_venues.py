async def test_read_valid_venues(async_client, synthetic_venues):
    response = await async_client.get("/venues/")
    venues = response.json()
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert all(venue in synthetic_venues for venue in venues)