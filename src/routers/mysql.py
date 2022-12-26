from fastapi import APIRouter, Body, Depends, status

from src.controllers.authentication_controller import get_current_user
from src.models.authentication_models import User
from src.models.mysql_models import (
    MysqlCreateManyQuery,
    MysqlCreateQuery,
    MysqlQueries,
    MysqlQuery,
)
from src.services import mysql_service

router = APIRouter()


@router.post("/read-one", response_model=dict | None)
async def read_one(
    query: MysqlQuery = Body(...), _: User = Depends(get_current_user())
) -> dict | None:
    return mysql_service.read_one(query.statement, query.values)


@router.post("/read-many", response_model=list[dict])
async def read_many(
    query: MysqlQuery = Body(...), _: User = Depends(get_current_user())
) -> list[dict]:
    return mysql_service.read_many(query.statement, query.values, limit=query.limit)


@router.post("/run-one", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def run_one(
    query: MysqlQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mysql_service.run_one(query.statement, query.values)


@router.post("/run-many", status_code=status.HTTP_202_ACCEPTED, response_model=int)
async def run_many(
    queries: MysqlQueries = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mysql_service.run_many(queries.statements, queries.values)


@router.post("/create-one", status_code=status.HTTP_201_CREATED, response_model=int)
async def create_one(
    query: MysqlCreateQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mysql_service.create_one(query.table, query.item, strict=query.strict)


@router.post("/create-many", status_code=status.HTTP_201_CREATED, response_model=int)
async def create_many(
    query: MysqlCreateManyQuery = Body(...), _: User = Depends(get_current_user())
) -> int:
    return mysql_service.create_many(query.table, query.items, strict=query.strict)


@router.get("/schemas", response_model=dict | None)
async def list_schemas(_: User = Depends(get_current_user())) -> dict | None:
    return mysql_service.list_schemas()


@router.get("/constraints", response_model=list[dict])
async def list_constraints(_: User = Depends(get_current_user())) -> list[dict]:
    return mysql_service.list_constraints()
