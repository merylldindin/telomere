import os
from enum import Enum

from pydantic import BaseSettings, Field


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


ENVIRONMENT = Environment(os.getenv("ENVIRONMENT", "development"))

IS_DEVELOPMENT = ENVIRONMENT == Environment.DEVELOPMENT


class AuthenticationSettings(BaseSettings):
    username: str | None = None
    password: str | None = None
    secret_key: str = Field(default="secret-key")
    expiration_delta: int = Field(default=86400)

    class Config:
        env_prefix = "AUTHENTICATION_"


AUTHENTICATION_SETTINGS = AuthenticationSettings()
