import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config

from handlers import other_handlers, user_handlers


async def main() -> None:
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dispatcher = Dispatcher()
    
    dispatcher.include_router(user_handlers.router)
    dispatcher.include_router(other_handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())