from fastapi import APIRouter, Body, Depends, Query, status

from src.controllers.authentication_controller import get_current_user
from src.models.authentication_models import User
from src.models.mongodb_models import (
    MongodbCreateManyQuery,
    MongodbCreateQuery,
    MongodbDeleteQuery,
    MongodbReadQuery,
    MongodbUpdateQuery,
)
from src.services import mongodb_handler
from src.utils.formatters import dump_mongodb_results

router = APIRouter()


@router.post("/read-one", response_model=dict | None)
async def read_one(
    query: MongodbReadQuery = Body(...), _: User = Depends(get_current_user())
) -> dict | None:
    return dump_mongodb_results(
        mongodb_handler.read_one(query.collection, query.conditions)
    )


@router.post("/read-many", response_model=list[dict])
async def read_many(
    query: MongodbReadQuery = Body(...), _: User = Depends(get_current_user())
) -> list[dict]:
    return dump_mongodb_results(
        mongodb_handler.read_many(query.collection, query.conditions, limit=query.limit)
    )


@router.post(
    "/create-one", status_code=status.HTTP_201_CREATED, response_model=dict | None
)
async def create_one(
    query: MongodbCreateQuery = Body(...), _: User = Depends(get_current_user())
) -> dict | None:
    return dump_mongodb_results(
        mongodb_handler.create_one(query.collection, query.item)
    )


@router.post(
    "/create-many", status_code=status.HTTP_201_CREATED, response_model=list[dict]
)
async def create_many(
    query: MongodbCreateManyQuery = Body(...), _: User = Depends(get_current_user())
) -> list[dict]:
    return dump_mongodb_results(
        mongodb_handler.create_many(query.collection, query.items)
    )


@router.post("/update-one", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def update_one(
    query: MongodbUpdateQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.update_one(query.collection, query.condition, query.values)


@router.post("/update-many", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def update_many(
    query: MongodbUpdateQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.update_many(query.collection, query.condition, query.values)


@router.post("/rename-one", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def rename_one(
    query: MongodbUpdateQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.rename_one(query.collection, query.condition, query.values)


@router.post("/rename-many", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def rename_many(
    query: MongodbUpdateQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.rename_many(query.collection, query.condition, query.values)


@router.post("/delete-one", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def delete_one(
    query: MongodbDeleteQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.delete_one(query.collection, query.condition)


@router.post("/delete-many", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def delete_many(
    query: MongodbDeleteQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mongodb_handler.delete_many(query.collection, query.condition)


@router.delete("/collection", status_code=status.HTTP_202_ACCEPTED, response_model=None)
async def drop_collection(
    collection: str = Query(...), _: User = Depends(get_current_user())
) -> None:
    mongodb_handler.drop_collection(collection)


@router.get("/collections", response_model=list[str])
async def list_collections(_: User = Depends(get_current_user())) -> list[str]:
    return mongodb_handler.list_collections()
