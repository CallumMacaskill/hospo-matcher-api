from enum import Enum

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import InsertOneResult

from hospo_matcher.utils.data_models import settings
from hospo_matcher.utils.logger import log


class CollectionNames(str, Enum):
    sessions = "sessions"


class DB:
    def __init__(self):
        self._mongo_client = None
        self._db_client = None

    @property
    def mongo_client(self) -> MongoClient:
        if self._mongo_client is None:
            self._mongo_client = MongoClient(settings.MONGODB_CONNECTION_STRING)
            log.debug("Set MongoClient.")
        return self._mongo_client

    @property
    def db_client(self) -> Database:
        if self._db_client is None:
            self._db_client = self.mongo_client[settings.MONGODB_NAME]
            log.debug("Set database client.")
        return self._db_client

    def get_session_collection(self) -> Collection:
        log.debug(f"Getting collection {CollectionNames.sessions.value}.")
        return self.db_client.sessions


db = DB()
