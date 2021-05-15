from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    token: str = Field(..., env="TOKEN")
    psql_url: str = Field(..., env="PSQL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file="../.env")
