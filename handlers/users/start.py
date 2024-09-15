from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db, is_user_subscribed
from aiogram import types


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    user_id = message.from_user.id
    try:
        await db.add_user(fullname=message.from_user.full_name, telegram_id=message.from_user.id)
    except:
        pass
    if await is_user_subscribed(user_id):
        await message.answer(f"Xush kelibsiz, {message.from_user.full_name}!\n\nFilm IDsini kiriting:")
    else:
        channels = await db.get_all_channels()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"Obuna bo‘ling: {channel[0]}", url=f"https://t.me/{channel[0][1:]}")]
                for channel in channels
            ]
        )
        await message.answer(
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling !!!",
            reply_markup=keyboard
        )

