from httpx import AsyncClient
from pytest import fixture

from hospo_matcher.app import app
from hospo_matcher.utils.database import driver
from tests.data import test_db_client


@fixture(scope="session")
async def async_client(test_db_client):
    def _override_get_db_client():
        return test_db_client

    # Override dependency to use the custom test driver database client
    app.dependency_overrides[driver.get_db_client] = _override_get_db_client

    # Testing async endpoints that await MongoDB operations requires an async client.
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as async_client:
        yield async_client


@fixture(scope="session")
def anyio_backend():
    return "asyncio"
