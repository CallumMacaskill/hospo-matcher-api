from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from hospo_matcher.utils.data_models import Venue
from hospo_matcher.utils.database import driver
from hospo_matcher.utils.logger import log

router = APIRouter(prefix="/venues")

@router.get(path="/", response_model=list[Venue], response_model_by_alias=False)
async def read_venues(n: int = 10, db:Database=Depends(driver.get_db_client)) -> list[Venue]:
    """
    Retrieve a session object by matching code.
    """
    log.info(f"Reading {n} venues")
    collection = db.venues
    result = collection.find().limit(n)

    venues = list(result)

    if not venues:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Venues not found."
        )

    return venues
