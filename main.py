import json
from urllib.parse import urlencode

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ContentType, Message
from pydantic_settings import BaseSettings, SettingsConfigDict

from config import Settings

def main()  -> None:
    settings = Settings()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(send_photo_echo, F.photo)
    dp.message.register(process_sent_voice, F.voice)
    dp.message.register(process_sent_sticker, F.sticker)
    dp.message.register(send_echo_for_default)
    dp.message.register(process_start_command,F.command=="/start")
    dp.run_polling(bot)




def execute_telegram_api_request(settings: Settings, command: str, **params):
    encoded_params = urlencode(params)
    query = f"{settings.API_URL}{settings.BOT_TOKEN}/{command}?{encoded_params}"
    print(query)
    updates = requests.get(query).json()
    print(json.dumps(updates, separators=(",", ": "), indent="  "))


def print_aiogram_Message(message: Message) -> None:
    print(message.model_dump_json(indent=4, exclude_none=True))


# @dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    # print_aiogram_Message(message)
    await message.answer("Hi!\nI'm echoBot")


# @dp.message(Command(commands=["help"]))
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


async def send_echo_for_default(message: Message):
    print_aiogram_Message(message)
    await message.reply(text="received")


if __name__ == "__main__":
    main()
