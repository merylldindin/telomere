import os
import shutil

from fastapi import APIRouter, Depends, Query

from src.controllers import efs_controller
from src.controllers.authentication_controller import get_current_user
from src.models.authentication_models import User
from src.utils.exceptions import raise_400_exception

router = APIRouter()


@router.get("/tree", response_model=str)
async def walk_directory(
    path: str = Query(default="/app/efs"),
    _: User = Depends(get_current_user()),
) -> str:
    if not os.path.exists(path):
        raise_400_exception("Path does not exist")

    return efs_controller.walk_directory(path)


@router.post("/directory", response_model=None)
async def create_directory(
    path: str = Query(...),
    _: User = Depends(get_current_user()),
) -> None:
    if os.path.exists(path):
        raise_400_exception("Directory already exists")

    os.makedirs(path)


@router.delete("/directory", response_model=None)
async def delete_directory(
    path: str = Query(...),
    _: User = Depends(get_current_user()),
) -> None:
    if not os.path.exists(path):
        raise_400_exception("Directory does not exist")

    shutil.rmtree(path)
