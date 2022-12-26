from pydantic import BaseModel, BaseSettings


class MysqlSettings(BaseSettings):
    host: str | None = None
    database: str | None = None
    user: str | None = None
    password: str | None = None
    port: int = 3306

    class Config:
        env_prefix = "MYSQL_"


MYSQL_SETTINGS = MysqlSettings()


class StrictMysqlSettings(BaseModel):
    host: str
    database: str
    user: str
    password: str
    port: int = 3306
