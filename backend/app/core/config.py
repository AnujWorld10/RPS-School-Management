"""Configuration settings for the RPS School application."""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "RPS School Roh"

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "mysql"
    DB_NAME: str = "rps_school"

    # Allow an explicit DATABASE_URL to override the constructed URL
    DATABASE_URL: Optional[str] = None

    SECRET_KEY: str = "PpP16JHyN6hExgftR04QOGO8WDCq58bDEnHWY4fEUCo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        """Return a SQLAlchemy async database URL.

        Preference order:
        1. `DATABASE_URL` environment variable
        2. Construct a sqlite+aiosqlite URL using `DB_NAME` (for local dev)
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # If no explicit DATABASE_URL is set, construct a MySQL async URL
        # using aiomysql (suitable for local or remote MySQL servers).
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
