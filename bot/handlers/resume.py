from asgiref.sync import sync_to_async
from aiogram import Router, F
from aiogram.types import Message
from portfolio.models import ResumeEducation

router = Router()
ADMIN_IDS = [7294943620]

@router.message(F.text == "/resume")
async def list_resume(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    resumes = await sync_to_async(list)(ResumeEducation.objects.all())
    if not resumes:
        await message.reply("Hali resume yo‘q.")
        return
    
    msg = "\n".join([f"{r.id}. {r.study_name}" for r in resumes])
    await message.reply(f"Resume ro'yxati:\n{msg}")

@router.message(F.text.startswith("/add_resume"))
async def add_resume(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Iltimos, nom yozing: /add_resume <study_name>")
        return
    
    resume = await sync_to_async(ResumeEducation.objects.create)(study_name=parts[1], study_year=0, study_about="")
    await message.reply(f"Resume '{resume.study_name}' qo‘shildi!")

@router.message(F.text.startswith("/delete_resume"))
async def delete_resume(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Iltimos, ID raqamini yozing: /delete_resume <id>")
        return

    resume_id = int(parts[1])
    try:
        resume = await sync_to_async(ResumeEducation.objects.get)(id=resume_id)
        await sync_to_async(resume.delete)()
        await message.reply(f"Resume '{resume.study_name}' o‘chirildi!")
    except ResumeEducation.DoesNotExist:
        await message.reply("Bunday ID topilmadi.")
