"""
Name this module as helper functions while the scope is not certain.
"""

from bson import ObjectId
from fastapi import HTTPException, status


def str_to_bson_ids(ids: list[str]) -> list[ObjectId]:
    """
    Check that venue IDs are valid BSON ObjectIds and convert to strings.
    """
    venue_bson_ids = []
    for venue_id in ids:
        if ObjectId.is_valid(venue_id):
            venue_bson_ids.append(ObjectId(venue_id))
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"ID is not a valid BSON ObjectId - '{venue_id}'",
            )
    return venue_bson_ids
