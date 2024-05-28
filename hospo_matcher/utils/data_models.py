from datetime import datetime
from typing import Annotated, Optional

import pydantic
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGODB_CONNECTION_STRING: str
    MONGODB_NAME: str

    model_config = SettingsConfigDict(env_file=".env.local")


PyObjectId = Annotated[str, BeforeValidator(str)]


class Session(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    code: str
    location: str = "WGN"
    date_time: str = Field(
        default_factory=lambda: datetime.now()
        .astimezone()
        .strftime("%m/%d/%Y, %H:%M:%S")
    )  # NZST

    model_config = ConfigDict(populate_by_name=True)


settings = Settings()
