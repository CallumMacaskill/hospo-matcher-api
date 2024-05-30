from pymongo.collection import Collection
from pymongo.results import InsertOneResult


def create_document(collection: Collection, data: dict) -> InsertOneResult:
    """
    Insert a document into a collection
    """
    result = collection.insert_one(data)
    return result


def read_document(collection: Collection, query: dict) -> dict:
    result = collection.find_one(query)
    return result
