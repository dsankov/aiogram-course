import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import (
    KICKED,
    MEMBER,
    ChatMemberUpdatedFilter,
    Command,
    CommandStart,
)
from aiogram.types import ChatMemberUpdated, ContentType, Message

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


# TODO Why not `async def main`?
def main() -> None:
    settings = Settings()
    bot = Bot(token=settings.BOT_TOKEN)
    dispatcher = Dispatcher()
    message_handlers = [
        (process_start_command, CommandStart()),
        (process_help_command, Command(commands=["help", "rules"])),
        (process_cancel_command, Command("cancel")),
        (process_stat_command, Command("stat")),
        (process_positive_ansver, F.text.lower().in_(["y", "yes"])),
        (
            process_numbers_answer_in_game,
            lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100,
        ),
        (process_other_message_input, F.text),
    ]

    for handler, filter in message_handlers:
        dispatcher.message.register(handler, filter)

    event_handlers = [
        (
            process_user_blocked_bot,
            ChatMemberUpdatedFilter(member_status_changed=KICKED),
        ),
        (
            process_user_unblock_bot,
            ChatMemberUpdatedFilter(member_status_changed=MEMBER),
        ),
    ]

    for handler, filter in event_handlers:
        dispatcher.my_chat_member.register(handler, filter)

    dispatcher.run_polling(bot)



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
        await message.answer(
            text=f"You loose. It was {user['secret_number']}\nAnother try?"
        )


async def process_other_message_input(message: Message):
    await message.answer(text="xm.. unecpected input")


async def process_user_blocked_bot(event: ChatMemberUpdated):
    print(f"Пользователь {event.from_user.id} заблокировал бота")


async def process_user_unblock_bot(event: ChatMemberUpdated):
    print(f"Пользователь {event.from_user.id} разблокировал бота")
    await event.answer(text=f"Welcome back {event.from_user.first_name}")


if __name__ == "__main__":
    main()
