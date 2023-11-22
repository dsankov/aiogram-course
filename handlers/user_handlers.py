from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_EN
from aiogram import Router

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_EN["/start"])
    
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_EN["/help"])
    


