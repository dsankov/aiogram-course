import json
import requests
import time

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env")
    
API_URL = "https://api.telegram.org/bot"
TEXT = "Update received"
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int
settings = Settings()

while counter < MAX_COUNTER:
    print("attempt=", counter)
    updates = requests.get(f"{API_URL}{settings.BOT_TOKEN}/getUpdates?offset={offset+1}").json()
    
    print(json.dumps(updates, separators=(",", "-"), indent="  "))
    
    if updates['result']:
        for result in updates['result']:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            requests.get(f"{API_URL}{settings.BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={result['message']['from']['first_name']} says {result['message']['text']}")
            
    time.sleep(5)
    counter += 1