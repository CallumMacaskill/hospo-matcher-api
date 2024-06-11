from hospo_matcher.app import app
from hospo_matcher.utils.data_models import settings
from hospo_matcher.utils.database import Driver, driver

from pytest import fixture
from httpx import AsyncClient

from tests.data import initialise_db


@fixture(scope="session")
async def async_client():
    def _override_get_db_client():
        return test_driver.get_db_client("test_db_test")
    
    # Initialise test database
    await initialise_db(settings.MONGODB_TEST_NAME)

    # Override dependency to use the custom test driver database client
    test_driver = Driver()
    app.dependency_overrides[driver.get_db_client] = _override_get_db_client

    # Testing async endpoints that await MongoDB operations requires an async client.
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as async_client:
        yield async_client

    # Tear down db
    test_driver.mongo_client.drop_database(settings.MONGODB_TEST_NAME)


@fixture(scope="session")
def anyio_backend():
    return 'asyncio'
