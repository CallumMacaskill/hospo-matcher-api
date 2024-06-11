from hospo_matcher.utils.data_models import Session, Venue
from hospo_matcher.utils.database import Driver
from hospo_matcher.utils.data_models import RegionCodes
from hospo_matcher.utils.logger import log

from random import randint, choice
import asyncio

from argparse import ArgumentParser

async def initialise_db(db_name: str):
    """
    Create a new MongoDB database with collections and pre-filled data.

    Helpful for initialising new dev databases.
    """
    # Construct test db and collections and load data
    driver = Driver()
    db = driver.get_db_client(db_name)
    log.info(f"Created db {db_name}")

    # Initialise venues data
    venues = generate_synthetic_venues()
    venues_result = await db.venues.insert_many(venues)
    log.info(f"Inserted {len(venues_result.inserted_ids)} venues")

    # Initialise sessions collection and data
    await db.sessions.create_index("code", unique=True)
    sessions = generate_synthetic_sessions(venues_result.inserted_ids)
    sessions_result = await db.sessions.insert_many(sessions)
    log.info(f"Inserted {len(sessions_result.inserted_ids)} sessions")

    return db

def generate_synthetic_venues(n_venues: int = 50) -> list[dict]:
    # Generate venues
    region_codes = list(RegionCodes)
    venues = []
    for i in range(n_venues):
        venue = Venue(
            id=str(i),
            name=f"Venue #{i}",
            region=choice(region_codes),
            hour_open=randint(6, 10),
            hour_closed=randint(17, 24)
        )
        venues.append(venue.model_dump())
    return venues    

def generate_synthetic_sessions(venue_ids: list[str], n_sessions: int = 5) -> list[dict]:
    # Generate venues
    region_codes = list(RegionCodes)
    sessions = []
    for i in range(n_sessions):
        session = Session(
            code=f"session_{i}",
            location=choice(region_codes),
            user_votes={f"User {i}{j}": [str(choice(venue_ids)) for k in range(randint(5, 10))] for j in range(randint(2, 10))}
        )
        sessions.append(session.model_dump())
    return sessions

if __name__=="__main__":
    # Get inputs
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--db-name",
        help="Name of the MongoDB database to be created."
    )
    args = arg_parser.parse_args()
    db_name = args.db_name

    # Create new db
    asyncio.run(initialise_db(db_name))
