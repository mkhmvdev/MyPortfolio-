from aiogram import Router, F
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async
from portfolio.models import Portfolio
from django.core.files.base import ContentFile
import html

router = Router()

class PortfolioStates(StatesGroup):
    name = State()
    image = State()
    git_url = State()

@router.message(F.text == "/portfolio_add")
async def start_add_portfolio(message: Message, state: FSMContext):
    await message.reply("Portfolio nomini kiriting:")
    await state.set_state(PortfolioStates.name)

@router.message(PortfolioStates.name)
async def portfolio_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply("Rasmni yuboring (photo sifatida):")
    await state.set_state(PortfolioStates.image)

@router.message(PortfolioStates.image, F.content_type == ContentType.PHOTO)
async def portfolio_image(message: Message, state: FSMContext):
    await state.update_data(image_file_id=message.photo[-1].file_id)
    await message.reply("GitHub URL kiriting:")
    await state.set_state(PortfolioStates.git_url)

@router.message(PortfolioStates.git_url)
async def portfolio_git_url(message: Message, state: FSMContext):
    data = await state.get_data()
    file_id = data['image_file_id']

    portfolio = Portfolio(
        name=data['name'],
        git_url=message.text
    )

    file = await message.bot.get_file(file_id)
    downloaded_file = await message.bot.download_file(file.file_path)
    portfolio.image.save(f"{portfolio.name}.jpg", ContentFile(downloaded_file.read()), save=False)

    await sync_to_async(portfolio.save)()
    await message.reply(f"Portfolio '{html.escape(portfolio.name)}' saqlandi!")
    await state.clear()



@router.message(F.text == "/portfolio_list")
async def list_portfolios(message: Message):
    portfolios = await sync_to_async(list)(Portfolio.objects.all())
    if not portfolios:
        await message.reply("Portfolio ro‘yxati bo‘sh")
        return
    text = "📁 Portfolio ro‘yxati:\n\n"
    for p in portfolios:
        text += f"ID: {p.id}\nNom: {p.name}\nGitHub: {p.git_url}\n\n"
    await message.reply(text)


@router.message(F.text.startswith("/portfolio_delete"))
async def delete_portfolio(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("Foydalanish: /portfolio_delete <id>")
        return
    portfolio_id = int(parts[1])
    portfolio = await sync_to_async(Portfolio.objects.filter(id=portfolio_id).first)()
    if not portfolio:
        await message.reply("Bunday ID mavjud emas")
        return
    await sync_to_async(portfolio.delete)()
    await message.reply(f"Portfolio '{portfolio.name}' o‘chirildi")
    
