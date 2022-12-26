from pydantic import BaseModel, PositiveInt


class MongodbCollection(BaseModel):
    collection: str


class MongodbReadQuery(MongodbCollection):
    conditions: dict = {}
    limit: PositiveInt = 1000


class MongodbCreateQuery(MongodbCollection):
    item: dict


class MongodbCreateManyQuery(MongodbCollection):
    items: list[dict]


class MongodbUpdateQuery(MongodbCollection):
    condition: dict
    values: dict


class MongodbDeleteQuery(MongodbCollection):
    condition: dict
