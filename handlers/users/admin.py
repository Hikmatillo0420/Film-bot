from loader import dp, db
from aiogram import types, F
from aiogram.filters import Command
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import *
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates  # FSM state for reklama


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=admin_button())


@dp.message(F.text == "🛎 Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = await db.count_users()
    count = count_result[0]
    await message.answer(f"Foydalanuvchilar soni: {count}")


@dp.message(F.text == "📌Majburiy Obuna", IsBotAdmin())
async def force_channel(message: types.Message):
    await message.answer("🔝 Majburiy obunalar qo'shish bo'limi:", reply_markup=majburiy_obuna())


#
# @dp.message(F.text == "📤 Reklama yuborish", IsBotAdmin())
# async def reklama_start(message: types.Message, state: FSMContext):
#     await message.answer("Reklama yuborish uchun rasm, video yoki matn yuboring.")
#     await state.set_state(FilmAddStates.content)
