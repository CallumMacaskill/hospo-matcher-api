from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from hospo_matcher.utils.data_models import Venue, VenueFilters
from hospo_matcher.utils.database import driver
from hospo_matcher.utils.logger import log
from hospo_matcher.utils.dependencies import DBClientDep

router = APIRouter(prefix="/venues")

@router.post(path="/sample", response_model=list[Venue], response_model_by_alias=False)
async def read_venues(db:DBClientDep, filters: VenueFilters) -> list[Venue]:
    """
    Retrieve a configurable combination of random venues.
    """
    log.info(f"Reading venues:\nExcluding ids:{filters.exclude_ids}\nIncluding ids:{filters.include_ids}")
    venues = []

    # Retrieve n venues with ID exclusion
    exclude_ids = [ObjectId(x) for x in filters.exclude_ids]
    result = db.venues.find({"_id": {"$nin": exclude_ids}}).limit(filters.n)
    venues.extend(await result.to_list(filters.n))

    # Retrieve included venues
    include_ids = [ObjectId(x) for x in filters.include_ids]
    result = db.venues.find({"_id": {"$in": include_ids}})
    venues.extend(await result.to_list(len(include_ids)))

    if not venues:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Venues not found."
        )

    return venues
