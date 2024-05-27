from fastapi import APIRouter

from hospo_matcher.utils.data_models import Session
from hospo_matcher.utils.logger import log

router = APIRouter(prefix="/sessions")


@router.post(path="/")
async def create_session(session: Session):
    log.info(f"Creating session! {session.model_dump()}")
