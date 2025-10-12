from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bot_token: str = ""
    allowed_updates: list = []
    admins_list: list[int] = Field(default_factory=list)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
