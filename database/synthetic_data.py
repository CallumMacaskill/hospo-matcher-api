from random import choice, randint

from motor.motor_asyncio import AsyncIOMotorDatabase

from hospo_matcher.utils.data_models import RegionCodes, Session, Venue
from hospo_matcher.utils.logger import log


async def load_synthetic_venues(db_client: AsyncIOMotorDatabase) -> list[str]:
    """
    Generate and insert synthetic venues into test db.
    """
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
    result = await db_client.venues.insert_many(venues)
    log.info(f"Inserted {len(result.inserted_ids)} venues")
    return [str(id) for id in result.inserted_ids]


async def load_synthetic_sessions(
    db_client: AsyncIOMotorDatabase, venue_ids: list[str]
) -> list[str]:
    """
    Generate and insert synthetic sessions into test db.
    """
    region_codes = list(RegionCodes)
    sessions = []

    for i in range(5):
        user_votes = {}
        num_users = randint(2, 10)

        # Create votes using venue IDs
        for j in range(num_users):
            user_key = f"User {i}{j}"
            num_venues = randint(5, 10)
            venues = [str(choice(venue_ids)) for _ in range(num_venues)]
            user_votes[user_key] = venues

        session = Session(
            code=f"session_{i}",
            location=choice(region_codes),
            user_votes=user_votes,
        )
        sessions.append(session.model_dump(by_alias=True, exclude=["id"]))
    log.info(f"Created {len(sessions)} synthetic sessions")

    # Create unique code constraint and insert into collection
    await db_client.sessions.create_index("code", unique=True)
    result = await db_client.sessions.insert_many(sessions)
    log.info(f"Inserted {len(result.inserted_ids)} sessions")
    return [str(id) for id in result.inserted_ids]
