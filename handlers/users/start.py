from aiogram.dispatcher import router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.inline.buttons import subscription_button
from loader import dp, db, is_user_subscribed
from aiogram import types, F


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
        await message.answer(
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling !!!",
            reply_markup=await subscription_button()
        )


@dp.callback_query(lambda c: c.data == "check_subscription")
async def oldim(call: types.CallbackQuery):
    await call.message.delete()
    if await is_user_subscribed(call.from_user.id):
        await call.message.answer("Botdan foydalanishingiz mumkin😊")
    else:
        await call.message.answer("Iltimios! Foydalanish uchun quyidagi kanallarga a'zo bo'ling! 👇👇👇",
                                  reply_markup=await subscription_button())
