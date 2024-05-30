from fastapi import APIRouter, Depends, HTTPException, status

from hospo_matcher.controllers.crud import create_document, read_document
from hospo_matcher.utils.data_models import Session
from hospo_matcher.utils.database import db
from hospo_matcher.utils.logger import log

router = APIRouter(prefix="/sessions")


@router.post(path="/")
async def create_session(
    session: Session, collection=Depends(db.get_session_collection)
):
    """
    Create a session document in the database.
    """
    data = session.model_dump(by_alias=True, exclude=["id"])
    log.info(f"Creating session with data:\n{data}")
    result = create_document(collection, data)
    log.info(f"Created session with id {result.inserted_id}")
    return str(result.inserted_id)


@router.get(path="/{code}", response_model=Session, response_model_by_alias=False)
async def read_session(
    code: str, collection=Depends(db.get_session_collection)
) -> Session:
    """
    Retrieve a session object by matching code.
    """
    log.info(f"Reading session with code {code}")
    query = {"code": code}
    result = read_document(collection, query)

    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Session with code {code} not found."
        )

    return result
