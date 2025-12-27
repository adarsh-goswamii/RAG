from fastapi import APIRouter
from app.routes.v1.admin import ingest

api_router = APIRouter()

api_router.include_router(ingest.router, prefix='/admin', tags=["Ingest data"])