import os
import sys
import django
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

# Django muhitini sozlash
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Handlerlarni import qilish
from bot.handlers.portfolio import router as portfolio_router
from bot.handlers.resume import router as resume_router
from bot.handlers.work import router as work_router

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Botni yaratish (aiogram 3.7+ sintaksis)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher
dp = Dispatcher()
dp.include_router(portfolio_router)
dp.include_router(resume_router)
dp.include_router(work_router)

# Start komandasi
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Admin botga xush kelibsiz\n\n"
        "/portfolio — portfolio ro‘yxati\n"
        "/resume — resume ro‘yxati\n"
        "/work — work ro‘yxati"
    )
    print(f"Bot start olindi, foydalanuvchi: {message.from_user.id}")

if __name__ == "__main__":
    dp.run_polling(bot)
