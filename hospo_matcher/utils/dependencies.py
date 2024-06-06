from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated

from hospo_matcher.utils.database import driver

# Database client dependency shared among endpoints
DBClientDep = Annotated[AsyncIOMotorDatabase, Depends(driver.get_db_client)]
