from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon import LEXICON_RU

button_yes = KeyboardButton(text=LEXICON_RU["yes_button"])
button_no = KeyboardButton(text=LEXICON_RU["no_button"])

yes_no_keyboard_builder = ReplyKeyboardBuilder()
yes_no_keyboard_builder.row(button_yes, button_no, width=2)
yes_no_keyboard: ReplyKeyboardMarkup = yes_no_keyboard_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True,
)

button_rock = KeyboardButton(text=LEXICON_RU["rock"])
button_paper = KeyboardButton(text=LEXICON_RU["paper"])
button_scissors = KeyboardButton(text=LEXICON_RU["scissors"])
button_lizard = KeyboardButton(text=LEXICON_RU["lizard"])
button_spock = KeyboardButton(text=LEXICON_RU["spock"])

game_keyboard_builder = ReplyKeyboardBuilder()
game_keyboard_builder.row(
    button_rock, button_paper, button_scissors, button_lizard, button_spock,
    width=3,
)
game_keyboard : ReplyKeyboardMarkup = game_keyboard_builder.as_markup()