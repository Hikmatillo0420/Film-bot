from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
        channels = await db.get_all_channels()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{channel[0]}", url=f"https://t.me/{channel[0][1:]}")]
                for channel in channels
            ],
        )
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")],

        )
        await message.answer(
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling !!!",
            reply_markup=keyboard,
        )


@dp.callback_query(F.data == "check_subscription")
async def check_subscription(callback: types.CallbackQuery):
    await callback.answer(cache_time=60)
    user_id = callback.from_user.id
    if await is_user_subscribed(user_id):
        await callback.message.delete()
        await callback.message.answer(
            f"👋 Salom, {callback.from_user.full_name}!\n\nMarhamat, kerakli kodni yuboring:")
    else:
        channels = await db.get_all_channels()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"{channel[0]}", url=f"https://t.me/{channel[0][1:]}")]
                for channel in channels
            ]
        )
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")]
        )
        await callback.message.edit_text(
            "❌ Siz hali ham obuna bo'lmadingiz! Iltimos, kanallarga obuna bo‘ling va yana tekshiring!",
            reply_markup=keyboard
        )
