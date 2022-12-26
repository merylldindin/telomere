from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str


class Credentials(BaseModel):
    username: str
    password: str


class JwtPayload(BaseModel):
    identity: str
    exp: datetime
