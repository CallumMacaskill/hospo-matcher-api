import pytest


@pytest.mark.anyio
async def test_read_sessions(async_client):
    response = await async_client.get("/venues/")
    assert response.status_code == 200
    assert len(response.json()) == 10
