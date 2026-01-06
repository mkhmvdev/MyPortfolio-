from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async
from portfolio.models import ResumeEducation
import html

router = Router()

class ResumeStates(StatesGroup):
    study_year = State()
    study_name = State()
    study_about = State()

@router.message(F.text == "/resume_add")
async def start_add_resume(message: Message, state: FSMContext):
    await message.reply("O‘qish yilini kiriting:")
    await state.set_state(ResumeStates.study_year)

@router.message(ResumeStates.study_year)
async def resume_year(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Faqat raqam kiriting (yil):")
        return
    await state.update_data(study_year=int(message.text))
    await message.reply("Kurs yoki o‘quv markazi nomini kiriting:")
    await state.set_state(ResumeStates.study_name)

@router.message(ResumeStates.study_name)
async def resume_name(message: Message, state: FSMContext):
    await state.update_data(study_name=message.text)
    await message.reply("Qo‘shimcha ma’lumot yozing:")
    await state.set_state(ResumeStates.study_about)

@router.message(ResumeStates.study_about)
async def resume_about(message: Message, state: FSMContext):
    data = await state.get_data()
    resume = ResumeEducation(
        study_year=data['study_year'],
        study_name=data['study_name'],
        study_about=message.text
    )
    await sync_to_async(resume.save)()
    await message.reply(f"O‘qish tajribasi '{html.escape(resume.study_name)}' saqlandi!")
    await state.clear()


# Ko'rish
@router.message(F.text == "/resume_list")
async def list_resume(message: Message):
    resumes = await sync_to_async(list)(ResumeEducation.objects.all())
    if not resumes:
        await message.reply("Resume ro‘yxati bo‘sh")
        return
    text = "🎓 Resume ro‘yxati:\n\n"
    for r in resumes:
        text += f"ID: {r.id}\nYil: {r.study_year}\nNom: {r.study_name}\nDescription: {r.study_about}\n\n"
    await message.reply(text)

# O'chirish
@router.message(F.text.startswith("/resume_delete"))
async def delete_resume(message: Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("Foydalanish: /resume_delete <id>")
        return
    resume_id = int(parts[1])
    resume = await sync_to_async(ResumeEducation.objects.filter(id=resume_id).first)()
    if not resume:
        await message.reply("Bunday ID mavjud emas")
        return
    await sync_to_async(resume.delete)()
    await message.reply(f"Resume '{resume.study_name}' o‘chirildi")
