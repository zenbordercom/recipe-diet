from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    project_name: str = Field(default="Recipe Community API", description="Human readable service name")
    api_v1_prefix: str = "/api/v1"
    database_url: str = Field(
        default=f"sqlite:///{Path(__file__).resolve().parents[3] / 'data' / 'app.db'}",
        description="SQLAlchemy compatible database URL",
    )
    debug: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "RECIPE_API_"
        case_sensitive = False


@lru_cache
def get_settings(**overrides: Any) -> Settings:
    """Return a cached Settings instance."""

    return Settings(**overrides)


settings = get_settings()
