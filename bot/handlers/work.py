from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async
from portfolio.models import WorkExperience
import html

router = Router()

class WorkStates(StatesGroup):
    year = State()
    company_name = State()
    company_about = State()

@router.message(F.text == "/work_add")
async def start_add_work(message: Message, state: FSMContext):
    await message.reply("Ish yilini kiriting:")
    await state.set_state(WorkStates.year)

@router.message(WorkStates.year)
async def work_year(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Faqat raqam kiriting (yil):")
        return
    await state.update_data(year=int(message.text))
    await message.reply("Company nomini kiriting:")
    await state.set_state(WorkStates.company_name)

@router.message(WorkStates.company_name)
async def work_company_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await message.reply("Ish haqida qisqacha ma'lumot yozing:")
    await state.set_state(WorkStates.company_about)

@router.message(WorkStates.company_about)
async def work_about(message: Message, state: FSMContext):
    data = await state.get_data()
    work = WorkExperience(
        company_year=data['year'],
        company_name=data['company_name'],
        company_about=message.text
    )
    await sync_to_async(work.save)()
    await message.reply(f"Ish tajribasi '{html.escape(work.company_name)}' saqlandi!")
    await state.clear()


@router.message(F.text == "/work_list")
async def list_work(message: Message):
    works = await sync_to_async(list)(WorkExperience.objects.all())
    if not works:
        await message.reply("Work ro‘yxati bo‘sh")
        return
    text = "💼 Work ro‘yxati:\n\n"
    for w in works:
        text += f"ID: {w.id}\nYil: {w.company_year}\nNom: {w.company_name}\nDescription: {w.company_about}\n\n"
    await message.reply(text)

@router.message(F.text.startswith("/work_delete"))
async def delete_work(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("Foydalanish: /work_delete <id>")
        return
    work_id = int(parts[1])
    work = await sync_to_async(WorkExperience.objects.filter(id=work_id).first)()
    if not work:
        await message.reply("Bunday ID mavjud emas")
        return
    await sync_to_async(work.delete)()
    await message.reply(f"Work '{work.company_name}' o‘chirildi")
    