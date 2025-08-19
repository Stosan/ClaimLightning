import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Basic service settings
    APP_NAME: str = "ClaimLightning"
    API_V1_STR: str = "/api/v1"
    # Model settings
    MODEL_NAME: str = "gpt-5"
    MAX_HISTORY_TOKENS: int = 1000
    # Runtime & infra
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    # Security
    ALLOWED_ORIGINS: str = "*"

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
