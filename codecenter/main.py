
from aiogram import Dispatcher, Bot
import asyncio
from codecenter.script import router

BOT_TOKEN = "8879128365:AAF5QOV-ZA8AoO0WVuBbH1gsVU6B81Sz9Pw"
bot = Bot(token=BOT_TOKEN)


db = Dispatcher()
db.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    await db.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())