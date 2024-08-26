from loader import dp, db
from aiogram import types, F
from aiogram.filters import Command
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import *


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=admin_button())


@dp.message(F.text == "Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = await db.count_users()
    count = count_result[0]
    await message.answer(f"Foydalanuvchilar soni: {count}")


#
#
# @dp.message(F.text == "Reklama yuborish", IsBotAdmin())
# async def reklama(message: types.Message):
#     await message.answer("Qanday turdagi xabar joylashtirmoqchisiz\nTanlang..... ")
#
#
# @dp.message(F.text == "🔙 ortga", IsBotAdmin())
# async def start_admin_bot(message: types.Message):
#     await message.answer("🔝 Admin panel....", reply_markup=admin_button())
