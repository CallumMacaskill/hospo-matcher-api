from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGODB_CONNECTION_STRING: str

    model_config = SettingsConfigDict(env_file=".env.local")


class Session(BaseModel):
    code: str
    location: str = "WGN"
    date_time: str = Field(
        default_factory=lambda: datetime.now()
        .astimezone()
        .strftime("%m/%d/%Y, %H:%M:%S")
    )  # NZST


settings = Settings()
