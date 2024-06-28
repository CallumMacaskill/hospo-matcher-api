import asyncio

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from pytest import fixture

from database.synthetic_data import load_synthetic_sessions, load_synthetic_venues
from hospo_matcher.app import app
from hospo_matcher.utils.data_models import settings
from hospo_matcher.utils.database import Driver, driver
from hospo_matcher.utils.logger import log


@pytest.fixture(scope="session", autouse=True)
async def synthetic_venues(test_db_client: AsyncIOMotorDatabase) -> list[str]:
    """
    Generate and insert synthetic venues into test db.
    """
    return await load_synthetic_venues(test_db_client)


@pytest.fixture(scope="session", autouse=True)
async def synthetic_sessions(
    test_db_client: AsyncIOMotorDatabase, synthetic_venues: list[str]
) -> list[str]:
    """
    Generate and insert synthetic sessions into test db.
    """
    venue_ids = [venue["id"] for venue in synthetic_venues]
    return await load_synthetic_sessions(test_db_client, venue_ids)


@pytest.fixture(scope="session")
async def test_db_client():
    """
    Create a new MongoDB database with collections and pre-filled data.

    Helpful for initialising new dev databases.
    """
    # Construct test db and collections and load data
    driver = Driver()
    client = driver.mongo_client
    client.get_io_loop = asyncio.get_event_loop
    db = driver.get_db_client(settings.MONGODB_TEST_NAME)
    log.info(f"Providing db client for {settings.MONGODB_TEST_NAME}")

    # Provide database client for tests
    yield db

    # Tidy up database after tests have run
    driver.mongo_client.drop_database(settings.MONGODB_TEST_NAME)
    log.info(f"Dropped db {settings.MONGODB_TEST_NAME}")


@pytest.fixture(scope="session")
async def async_client(test_db_client):
    """
    API client with overridden db client.
    """

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
