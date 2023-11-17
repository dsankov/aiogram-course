import json
import time
from urllib.parse import urlencode


import jsonpickle
import requests
from aiogram import Bot, Dispatcher, F

# from magic_filter import F
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


def execute_telegram_api_request(settings: Settings, command: str, **params):
    encoded_params = urlencode(params)
    query = f"{settings.API_URL}{settings.BOT_TOKEN}/{command}?{encoded_params}"
    print(query)
    updates = requests.get(query).json()
    print(type(updates))
    print(json.dumps(updates, separators=(",", ": "), indent="  "))


def print_aiogram_Message(message: Message) -> None:
    # message_str: str = jsonpickle.encode(message)
    # message_dict = json.loads(message_str)
    # print(json.dumps(message_dict, separators=(",", ": "), indent="  "))

    print(message.model_dump_json(indent=4, exclude_none=True))


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    # print_aiogram_Message(message)
    await message.answer("Hi!\nI'm echoBot")


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer("Type anything and I'll send it back")


async def send_photo_echo(message: Message):
    print_aiogram_Message(message)
    await message.reply_photo(message.photo[0].file_id)


async def process_sent_voice(message: Message):
    print_aiogram_Message(message)
    await message.answer(text="You sent a voice message")
    
async def process_sent_sticker(message: Message):
    print_aiogram_Message(message)
    await message.answer(text="sticker received")


dp.message.register(send_photo_echo, F.photo)
dp.message.register(process_sent_voice, F.voice)
dp.message.register(process_sent_sticker, F.sticker)


@dp.message()
async def send_echo(message: Message):
    print_aiogram_Message(message)
    await message.reply(text=message.text)


if __name__ == "__main__":
    # execute_telegram_api_request(settings, "getUpdates", offset=-1)
    dp.run_polling(bot)
    # execute_telegram_api_request(settings,command="sendMessage",chat_id=112033576, text="Привет от Димаса")
