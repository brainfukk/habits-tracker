import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.core.config import TELEGRAM_BOT_API_TOKEN

bot = Bot(token=TELEGRAM_BOT_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def send_message(chat_id: int, text: str, reply_markup):
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


def sync_send_message(chat_id, text, reply_markup=None):
    return asyncio.run(send_message(chat_id, text, reply_markup))
