from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
    

class TgBot(BaseModel):
    token: str
    
class Config(BaseModel):
    tg_bot: TgBot
    
def load_config():
    settings = Settings()
    return Config(tg_bot=TgBot(token=settings.BOT_TOKEN))
