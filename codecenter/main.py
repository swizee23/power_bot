
from aiogram import Dispatcher, Bot
import asyncio
from codecenter.motivation import router_motivation
from codecenter.thinking import router
from codecenter.woman import router_woman

BOT_TOKEN = "8879128365:AAF5QOV-ZA8AoO0WVuBbH1gsVU6B81Sz9Pw"
bot = Bot(token=BOT_TOKEN)


db = Dispatcher()
db.include_router(router)
db.include_router(router_motivation)
db.include_router(router_woman)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    await db.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())