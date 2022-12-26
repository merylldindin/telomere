from urllib.parse import quote_plus

import pymongo
from bson.objectid import ObjectId

from .settings import MONGODB_SETTINGS
from .utils import build_host_url


class MongodbService:
    def __init__(self) -> None:
        self.is_undefined = any(
            value is None for value in MONGODB_SETTINGS.dict().values()
        )

    def _connect(self) -> None:
        self._client = pymongo.MongoClient(build_host_url(MONGODB_SETTINGS))
        self._database = self._client[MONGODB_SETTINGS.database]

    def read_one(self, collection: str, conditions: dict | None = None) -> dict | None:
        return self._database[collection].find_one(
            {} if conditions is None else conditions
        )

    def read_many(
        self, collection: str, conditions: dict | None = None, limit: int = 1000
    ) -> list[dict]:
        return list(
            self._database[collection].find(
                {} if conditions is None else conditions, limit=limit
            )
        )

    def create_one(self, collection: str, item: dict) -> ObjectId | None:
        return self._database[collection].insert_one(item).inserted_id

    def create_many(self, collection: str, items: list[dict]) -> list[ObjectId]:
        return self._database[collection].insert_many(items).inserted_ids

    def update_one(self, collection: str, condition: dict, values: dict) -> int:
        return (
            self._database[collection]
            .update_one(condition, {"$set": values})
            .modified_count
        )

    def update_many(self, collection: str, condition: dict, values: dict) -> int:
        return (
            self._database[collection]
            .update_many(condition, {"$set": values})
            .modified_count
        )

    def rename_one(self, collection: str, condition: dict, values: dict) -> int:
        return (
            self._database[collection]
            .update_one(condition, {"$rename": values})
            .modified_count
        )

    def rename_many(self, collection: str, condition: dict, values: dict) -> int:
        return (
            self._database[collection]
            .update_many(condition, {"$rename": values})
            .modified_count
        )

    def delete_one(self, collection: str, condition: dict) -> int:
        return self._database[collection].delete_one(condition).deleted_count

    def delete_many(self, collection: str, condition: dict) -> int:
        return self._database[collection].delete_many(condition).deleted_count

    def drop_collection(self, collection: str) -> None:
        self._database.drop_collection(collection)

    def list_collections(self) -> list[str]:
        return self._database.list_collection_names()
