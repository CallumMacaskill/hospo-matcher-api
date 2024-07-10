from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from hospo_matcher.utils.data_models import Session, UserVotes
from hospo_matcher.utils.dependencies import DBClientDep
from hospo_matcher.utils.logger import log

router = APIRouter(prefix="/sessions")


@router.post(path="/")
async def create_session(session: Session, db: DBClientDep) -> str:
    """
    Create a session document in the database.
    """
    data = session.model_dump(by_alias=True, exclude=["id"])

    # Check if session code already exists
    existing_session = await db.sessions.find_one({"code": data["code"]})
    if existing_session:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Code already exists in session with ID - '{str(existing_session['_id'])}'",
        )

    log.info(f"Creating session with data:\n{data}")
    result = await db.sessions.insert_one(data)
    log.info(f"Created session with id {result.inserted_id}")
    return str(result.inserted_id)


@router.get(path="/{code}", response_model=Session, response_model_by_alias=False)
async def read_session(code: str, db: DBClientDep) -> Session:
    """
    Retrieve a session object by matching code.
    """
    log.info(f"Reading session with code {code}")
    query = {"code": code}
    result = await db.sessions.find_one(query)

    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Session with code {code} not found."
        )

    return result


@router.post(path="/{code}/{user_id}")
async def submit_votes(
    code: str, user_id: str, votes: UserVotes, db: DBClientDep
) -> str:
    """
    Add user's unique vote information to associated session object
    """
    log.info(f"Adding votes to session {code} under user {user_id}")

    # Get user's existing votes
    session_doc = await db.sessions.find_one({"code": code})
    if session_doc is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Session with code {code} not found."
        )
    session = Session(**session_doc)

    # Add new votes
    votes.upvotes.update(session.user_votes[user_id])
    session.user_votes[user_id] = list(votes.upvotes)

    # Update session document
    result = await db.sessions.update_one(
        {"_id": ObjectId(session.id)}, {"$set": {"user_votes": session.user_votes}}
    )

    if result.modified_count != 1:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Vote update operation modified {result.modified_count} documents.",
        )

    return session.id
