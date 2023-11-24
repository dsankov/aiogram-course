import asyncio
import logging
# from venv import logger

from aiogram import Bot, Dispatcher
from aiogram.filters import command
from aiogram.types import BotCommand
from config_data.config import Config, load_config

from handlers import other_handlers, user_handlers

logger = logging.getLogger(__name__)


async def set_main_bot_menu(bot: Bot):
    bot_commands = [
        # BotCommand(command="", description=""),
        BotCommand(command="/help", description="Справка по работе бота"),
        BotCommand(command="/stat", description="Статистика игр"),
    ]
    await bot.set_my_commands(bot_commands)

async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)-8s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("starting bot")

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dispatcher = Dispatcher()

    dispatcher.startup.register(set_main_bot_menu)
    dispatcher.include_router(user_handlers.router)
    dispatcher.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
