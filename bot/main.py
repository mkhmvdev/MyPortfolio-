import os
import sys
import django
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
sys.path.append(os.path.dirname(BASE_DIR))
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from bot.handlers.portfolio import router as portfolio_router
from bot.handlers.resume import router as resume_router
from bot.handlers.work import router as work_router


BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


dp = Dispatcher()
dp.include_router(portfolio_router)
dp.include_router(resume_router)
dp.include_router(work_router)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Admin botga xush kelibsiz!\n\n"
        "Barcha komandalar uchun /help yozing."
    )
    print(f"Bot start olindi, foydalanuvchi: {message.from_user.id}")


@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "📌 Bot komandalari:\n\n"
        "Portfolio:\n"
        "/portfolio_add — portfolio qo‘shish\n"
        "/portfolio_list — portfolio ro‘yxati\n"
        "/portfolio_delete  — portfolio o‘chirish id orqali\n\n"
        "Resume:\n"
        "/resume_add — resume qo‘shish\n"
        "/resume_list — resume ro‘yxati\n"
        "/resume_delete  — resume o‘chirish id orqali\n\n"
        "Work:\n"
        "/work_add — work qo‘shish\n"
        "/work_list — work ro‘yxati\n"
        "/work_delete  — work o‘chirish id orqali"
    )
    await message.answer(help_text)

if __name__ == "__main__":
    dp.run_polling(bot)
