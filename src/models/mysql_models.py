from pydantic import BaseModel, PositiveInt


class MysqlQuery(BaseModel):
    statement: str
    values: tuple | None = None
    limit: PositiveInt = 1000


class MysqlQueries(BaseModel):
    statements: list[str]
    values: list[tuple | None] | None = None
    limit: PositiveInt = 1000


class MysqlCreateQuery(BaseModel):
    table: str
    item: dict
    strict: bool = True


class MysqlCreateManyQuery(BaseModel):
    table: str
    items: list[dict]
    strict: bool = True
