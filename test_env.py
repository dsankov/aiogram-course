import os
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    BOT_TOKEN: str
    API_URL: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
print(settings.BOT_TOKEN)
print(os.getenv('BOT_TOKEN'))