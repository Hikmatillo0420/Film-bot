import asyncio

from aiogram.fsm.context import FSMContext

from loader import dp, db
from aiogram import types, F
from aiogram.filters import Command
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import *
from states.film_add_states import FilmAddStates


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=admin_button())


@dp.message(F.text == "🛎 Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = db.count_users()
    count = count_result['total']
    await message.answer(f"👥  Foydalanuvchilar soni: {count}")


@dp.message(F.text == "📌Majburiy Obuna", IsBotAdmin())
async def force_channel(message: types.Message):
    await message.answer("🔝 Majburiy obunalar qo'shish bo'limi:", reply_markup=majburiy_obuna())


#
@dp.message(F.text == "📤 Reklama yuborish", IsBotAdmin())
async def reklama_start(message: types.Message, state: FSMContext):
    await message.answer("Reklama yuborish uchun rasm, video yoki matn yuboring.")
    await state.set_state(FilmAddStates.ask_ad_content)


@dp.message(FilmAddStates.ask_ad_content)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = db.select_all_users()
    count = 0
    for user in users:
        user_id = user['user_id']
        print("bular", user_id)
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
