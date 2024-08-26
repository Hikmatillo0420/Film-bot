from aiogram.filters import CommandStart
from loader import dp, db
from aiogram import types


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                         f"MeshpolvonFilm Bot -  orqali siz o'zingizga yoqqan kinoni topishingiz mumkin 🎬 !\n")
    await message.answer(f"Kino kodni yuboring !")
    try:
        await db.add_user(fullname=message.from_user.full_name, telegram_id=message.from_user.id)
    except:
        pass
