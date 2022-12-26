from fastapi import APIRouter, Body

from src.controllers.authentication_controller import (
    create_access_token,
    get_user_from_credentials,
)
from src.models.authentication_models import Credentials

router = APIRouter()


@router.get("/health", response_model=None)
async def health() -> None:
    return None


@router.post("/oauth", response_model=str)
async def login(credentials: Credentials = Body(...)) -> str:
    return create_access_token(get_user_from_credentials(credentials).username)
