from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str = "Appliation_Tracker_project"
    app_env:str = 'development'
    debug:bool = False

    supabase_url: str
    supabase_secret_key: str
    supabase_storage_bucket: str = "job-documents"

    dev_user_id:UUID

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

