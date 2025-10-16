from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    app_name: str = "Octopus Helpdesk"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "mysql+pymysql://user:password@localhost:3306/helpdesk"
    cors_origins: List[AnyHttpUrl] = []
    first_superuser_email: str = "admin@helpdesk.com"
    first_superuser_password: str = "admin123"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[AnyHttpUrl]:  # type: ignore[override]
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        if isinstance(v, list):
            return v
        return []


@lru_cache

def get_settings() -> Settings:
    return Settings()


settings = get_settings()
