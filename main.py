import json
import requests
import time

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer("Hi!\nI'm echoBot")

@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer("Type anything and I'll send it back")
    
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
    
if __name__ == "__main__":
    dp.run_polling(bot)