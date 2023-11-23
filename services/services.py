import random
from lexicon.lexicon import LEXICON_RU


def get_bot_choice() -> str:
    return random.choice(["rock", "paper", "scissors", "lizard", "spock"])


def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {
        "rock": ("scissors", "spock"),
        "paper": ("rock", "spock"),
        "scissors": ("paper", "lizard"),
        "lizard": ("paper", "spock"),
        "spock": ("rock", "scissors"),
    }
    if user_choice == bot_choice:
        return "draw"
    if bot_choice in rules[user_choice]:
        return "player_won"
    return "bot_won"
