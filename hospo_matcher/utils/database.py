from enum import Enum

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from hospo_matcher.utils.data_models import settings
from hospo_matcher.utils.logger import log


class Driver:
    def __init__(self, db_name=settings.MONGODB_NAME):
        self._mongo_client = None
        self._db_client = None
        self._db_name = db_name

    @property
    def mongo_client(self) -> MongoClient:
        if self._mongo_client is None:
            self._mongo_client = MongoClient(settings.MONGODB_CONNECTION_STRING)
            log.debug("Set MongoClient.")
        return self._mongo_client

    def get_db_client(self) -> Database:
        if self._db_client is None:
            self._db_client = self.mongo_client[self._db_name]
            log.debug("Set database client.")
        return self._db_client


driver = Driver()
