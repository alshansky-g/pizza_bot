from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bot_token: str = ""
    allowed_updates: list = []

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
