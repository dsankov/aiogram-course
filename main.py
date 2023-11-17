import json
import random
from urllib.parse import urlencode, uses_relative

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ContentType, Message
# from pydantic_settings import BaseSettings, SettingsConfigDict

from config import Settings

ATTEMPTS = 5
user = {
    "in_game": False,
    "secret_number": None,
    "attemts": None,
    "total_games": 0,
    "wins": 0,
}

# def print_aiogram_Message(message: Message) -> None:
#     print(message.model_dump_json(indent=4, exclude_none=True))


def main() -> None:
    settings = Settings()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(process_start_command, CommandStart())
    dp.message.register(process_help_command, Command(commands=["help", "rules"]))
    dp.message.register(process_stat_command, Command("stat"))
    dp.message.register(process_cancel_command, Command("cancel"))
    dp.message.register(process_positive_ansver, F.text.lower().in_(["y", "yes"]))
    dp.message.register(
        process_numbers_answer_in_game,
        lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100,
    )

    dp.message.register(process_other_input)
    dp.run_polling(bot)


def get_random_number() -> int:
    return random.randint(1, 100)


async def process_start_command(message: Message):
    await message.answer("Lets play Gues number.")


async def process_help_command(message: Message):
    await message.answer(f"1 up to 100. {ATTEMPTS} attampts")


async def process_stat_command(message: Message):
    await message.answer(
        text=f"Total games: {user['total_games']} \n" f"Wins: {user['wins']}"
    )


async def process_cancel_command(message: Message):
    if user["in_game"]:
        user["in_game"] = False
        await message.answer(text="You canceled the game. Another try?")
    else:
        await message.answer(text="Not playng now")


async def process_positive_ansver(message: Message):
    if not user["in_game"]:
        user["in_game"] = True
        user["secret_number"] = get_random_number()
        user["attemts"] = ATTEMPTS
        await message.answer(
            text=f"I guessed a number, try to guess it in {user['attemts']} tries"
        )
    else:
        await message.answer(text="We ary plaing right now. Only numbers or commands")


async def process_numbers_answer_in_game(message: Message):
    if not user["in_game"]:
        await message.answer(text="Not plaing. Lets have a try?")
        return

    input_number = int(message.text)
    await message.answer(str(input_number))

    if input_number == user["secret_number"]:
        user["in_game"] = False
        user["total_games"] += 1
        user["wins"] += 1
        await message.answer(text="You guessed! \nAnother try?")
    elif user["secret_number"] < input_number:
        user["attemts"] -= 1
        await message.answer(text="Less")
    else:
        user["attemts"] -= 1
        await message.answer(text="More")
    
    if user["attemts"] <= 0:
        user["in_game"] = False
        user["total_games"] += 1
        await message.answer(text=f"You loose. It was {user['secret_number']}\nAnother try?")
        
    

async def process_other_input(message: Message):
    await message.answer(text="xm.. unecpected input")


if __name__ == "__main__":
    main()
