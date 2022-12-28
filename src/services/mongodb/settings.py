from pydantic import BaseModel, BaseSettings


class MongodbSettings(BaseSettings):
    host: str | None = None
    database: str | None = None
    user: str | None = None
    tls_file: str | None = None
    password: str | None = None
    port: int = 27017

    class Config:
        env_prefix = "MONGODB_"


MONGODB_SETTINGS = MongodbSettings()


class StrictMongodbSettings(BaseModel):
    host: str
    database: str
    user: str
    password: str
    tls_file: str | None = None
    port: int = 27017
