import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    env: str            = os.getenv("ENV", "local")
    db_user: str        = os.getenv("DB_USER", "user")
    db_password: str    = os.getenv("DB_PASSWORD", "user")
    db_port: int        = os.getenv("DB_PORT", 9200)
    db_host: str        = os.getenv("DB_HOST", "http://localhost")
    db_name: str        = os.getenv("DB_NAME", "central_db")

    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_host: str = os.getenv("REDIS_HOST", "0.0.0.0")

    jwt_public_key: str = os.getenv("JWT_PUBLIC_KEY", "sample")

    auth_service_domain: str = os.getenv("AUTH_SERVICE_DOMAIN", "http://localhost:8000/v1/oauth/token")

    application_id: str = os.getenv("APPLICATION_ID", "app_1f62e9a874d748eaa0c88f3e11bb7c51")
    application_secret: str = os.getenv("APPLICATION_SECRET", "sec_4e93b0aa1c5f4a2da8f3e3e8bc602f9c")

    hash_secret_key: int = os.getenv("HASH_SECRET", 982374928374)

    embedding_dims: int    = os.getenv("EMBEDDING_DIMS", 768)
    embedding_model: str   = os.getenv("EMBEDDING_MODEL", 'nomic-embed-text')

@lru_cache
def get_settings():
    return BaseConfig()