import asyncio
from random import choice, randint

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from hospo_matcher.utils.data_models import RegionCodes, Session, Venue, settings
from hospo_matcher.utils.database import Driver
from hospo_matcher.utils.logger import log


@pytest.fixture(scope="session", autouse=True)
async def synthetic_venues(test_db_client: AsyncIOMotorDatabase) -> list[str]:
    # Generate objects
    region_codes = list(RegionCodes)
    venues = []
    for i in range(50):
        venue = Venue(
            name=f"Venue #{i}",
            region=choice(region_codes),
            hour_open=randint(6, 10),
            hour_closed=randint(17, 24),
        )
        venues.append(venue.model_dump(by_alias=True, exclude=["id"]))
    log.info(f"Created {len(venues)} synthetic venues")

    # Insert into collection
    result = await test_db_client.venues.insert_many(venues)
    log.info(f"Inserted {len(result.inserted_ids)} venues")
    return [str(id) for id in result.inserted_ids]


@pytest.fixture(scope="session", autouse=True)
async def synthetic_sessions(test_db_client: AsyncIOMotorDatabase, synthetic_venues: list[str]) -> list[str]:
    # Generate venues
    region_codes = list(RegionCodes)
    sessions = []
    for i in range(5):
        # TODO: Tidy user votes
        session = Session(
            code=f"session_{i}",
            location=choice(region_codes),
            user_votes={
                f"User {i}{j}": [
                    str(choice(synthetic_venues)) for k in range(randint(5, 10))
                ]
                for j in range(randint(2, 10))
            },
        )
        sessions.append(session.model_dump(by_alias=True, exclude=["id"]))
    log.info(f"Created {len(sessions)} synthetic sessions")

    # Create unique code constraint and insert into collection
    await test_db_client.sessions.create_index("code", unique=True)
    result = await test_db_client.sessions.insert_many(sessions)
    log.info(f"Inserted {len(result.inserted_ids)} sessions")
    return [str(id) for id in result.inserted_ids]


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
