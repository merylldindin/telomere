from datetime import timedelta
from hashlib import sha256
from typing import Callable

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.models.authentication_models import Credentials, JwtPayload, User
from src.utils.exceptions import raise_400_exception, raise_401_exception
from src.utils.settings import AUTHENTICATION_SETTINGS
from src.utils.timestamps import get_current_datetime


def _hash_password(password: str, encoding: str = "utf-8") -> str:
    return sha256(password.encode(encoding)).hexdigest()


def get_user_from_credentials(credentials: Credentials) -> User:
    if credentials.username != AUTHENTICATION_SETTINGS.username:
        raise_401_exception("Invalid username")

    hashed_password = _hash_password(credentials.password)

    if hashed_password != AUTHENTICATION_SETTINGS.password:
        raise_401_exception("Invalid password")

    return User(username=credentials.username)


def create_access_token(username: str, algorithm: str = "HS256") -> str:
    return jwt.encode(
        JwtPayload(
            identity=username,
            exp=get_current_datetime()
            + timedelta(seconds=AUTHENTICATION_SETTINGS.expiration_delta),
        ).dict(),
        AUTHENTICATION_SETTINGS.secret_key,
        algorithm=algorithm,
    )


def _decode_jwt(token: str, algorithm: str = "HS256") -> JwtPayload:
    return JwtPayload(
        **jwt.decode(token, AUTHENTICATION_SETTINGS.secret_key, algorithms=[algorithm])
    )


def _get_user_from_jwt(jwt_payload: JwtPayload) -> User:
    if jwt_payload.identity != AUTHENTICATION_SETTINGS.username:
        raise_401_exception("Unrecognized user")

    return User(username=jwt_payload.identity)


def get_current_user() -> Callable[[str], User]:
    def _determine_user_from_token(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/oauth")),
    ) -> User:
        try:
            return _get_user_from_jwt(_decode_jwt(token))

        except jwt.exceptions.ExpiredSignatureError:
            raise_401_exception()

        except jwt.exceptions.InvalidSignatureError:
            raise_400_exception()

    return _determine_user_from_token
