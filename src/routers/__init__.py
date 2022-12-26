from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import efs, mongodb, mysql, public
from src.utils.settings import IS_DEVELOPMENT

telomere = FastAPI(openapi_url="/openapi.json" if IS_DEVELOPMENT else "")

telomere.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

telomere.include_router(public.router)
telomere.include_router(efs.router, prefix="/efs")
telomere.include_router(mongodb.router, prefix="/mongodb")
telomere.include_router(mysql.router, prefix="/mysql")
