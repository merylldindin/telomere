from pydantic import BaseSettings, Field


class MongodbSettings(BaseSettings):
    host: str | None = None
    database: str | None = None
    user: str | None = None
    tls_file: str | None = None
    password: str | None = None
    port: int = Field(default=27017)

    class Config:
        env_prefix = "MONGODB_"


MONGODB_SETTINGS = MongodbSettings()
