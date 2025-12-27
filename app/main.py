from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from starlette.middleware.gzip import GZipMiddleware
from app.libs.elasticsearch_db import ElasticVectorDB, get_elastic_db

from app.config import get_settings
from app.routes.v1 import main as v1_routes

config = get_settings()
elastic_db: ElasticVectorDB | None = None

if config.env == "local":
    print("Server starting")

app = FastAPI(
    title="URL Shortener",
    description=""
)

@app.on_event("startup")
async def startup_event():
    get_elastic_db()
    print("Server started")


@app.on_event("shutdown")
async def shutdown_event():
    # do something
    print("Server stopped")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(v1_routes.api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001)