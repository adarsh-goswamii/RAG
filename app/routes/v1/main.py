from fastapi import APIRouter
from app.routes.v1.admin import main

api_router = APIRouter()

api_router.include_router(main.api_router, prefix='/v1')