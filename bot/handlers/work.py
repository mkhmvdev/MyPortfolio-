from asgiref.sync import sync_to_async
from aiogram import Router, F
from aiogram.types import Message
from portfolio.models import WorkExperience

router = Router()
ADMIN_IDS = [7294943620]

@router.message(F.text == "/work")
async def list_work(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    works = await sync_to_async(list)(WorkExperience.objects.all())
    if not works:
        await message.reply("Hali work experience yo‘q.")
        return
    
    msg = "\n".join([f"{w.id}. {w.company_name}" for w in works])
    await message.reply(f"Work Experience ro'yxati:\n{msg}")

@router.message(F.text.startswith("/add_work"))
async def add_work(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Iltimos, nom yozing: /add_work <company_name>")
        return
    
    work = await sync_to_async(WorkExperience.objects.create)(company_name=parts[1])
    await message.reply(f"Work '{work.company_name}' qo‘shildi!")

@router.message(F.text.startswith("/delete_work"))
async def delete_work(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Sizga ruxsat yo‘q.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Iltimos, ID raqamini yozing: /delete_work <id>")
        return

    work_id = int(parts[1])
    try:
        work = await sync_to_async(WorkExperience.objects.get)(id=work_id)
        await sync_to_async(work.delete)()
        await message.reply(f"Work '{work.company_name}' o‘chirildi!")
    except WorkExperience.DoesNotExist:
        await message.reply("Bunday ID topilmadi.")
