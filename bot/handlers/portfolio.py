from asgiref.sync import sync_to_async
from aiogram import Router, F
from aiogram.types import Message
from portfolio.models import Portfolio

router = Router()
ADMIN_IDS = [7294943620]

@router.message(F.text == "/portfolio")
async def list_portfolio(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    portfolios = await sync_to_async(list)(Portfolio.objects.all())
    if not portfolios:
        await message.reply("Hali portfolio yo‘q.")
        return
    
    msg = "\n".join([f"{p.id}. {p.name}" for p in portfolios])
    await message.reply(f"Portfolio ro'yxati:\n{msg}")

@router.message(F.text.startswith("/add_portfolio"))
async def add_portfolio(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Iltimos, nom yozing: /add_portfolio <nom>")
        return
    
    portfolio = await sync_to_async(Portfolio.objects.create)(name=parts[1])
    await message.reply(f"Portfolio '{portfolio.name}' qo‘shildi!")

@router.message(F.text.startswith("/delete_portfolio"))
async def delete_portfolio(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Iltimos, ID raqamini yozing: /delete_portfolio <id>")
        return

    portfolio_id = int(parts[1])
    try:
        portfolio = await sync_to_async(Portfolio.objects.get)(id=portfolio_id)
        await sync_to_async(portfolio.delete)()
        await message.reply(f"Portfolio '{portfolio.name}' o‘chirildi!")
    except Portfolio.DoesNotExist:
        await message.reply("Bunday ID topilmadi.")
