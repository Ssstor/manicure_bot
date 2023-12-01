import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.database.models import async_main
from app.handlers import router

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await async_main()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
