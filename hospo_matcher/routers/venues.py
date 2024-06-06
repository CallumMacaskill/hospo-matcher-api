from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from hospo_matcher.utils.data_models import Venue
from hospo_matcher.utils.database import driver
from hospo_matcher.utils.logger import log
from hospo_matcher.utils.dependencies import DBClientDep

router = APIRouter(prefix="/venues")

@router.get(path="/", response_model=list[Venue], response_model_by_alias=False)
async def read_venues(db:DBClientDep, n: int = 10, query: dict = {}) -> list[Venue]:
    """
    Retrieve a session object by matching code.
    """
    log.info(f"Reading {n} venues")
    result = db.venues.find(query).limit(n)

    venues = await result.to_list(n)

    if not venues:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Venues not found."
        )

    return venues
