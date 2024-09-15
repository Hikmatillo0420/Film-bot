from loader import dp, db, bot
from aiogram import types, F
from aiogram.filters import Command
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import *
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates  # FSM state for reklama


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=admin_button())


@dp.message(F.text == "Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = await db.count_users()
    count = count_result[0]
    await message.answer(f"Foydalanuvchilar soni: {count}")


@dp.message(F.text == "M.O kanal qo'shish", IsBotAdmin())
async def add_channel(message: types.Message, state: FSMContext):
    await message.answer("Telegram kanal username'ini kirting !!!\n\nMisol uchun: @kanal ")
    await state.set_state(FilmAddStates.kanal)


@dp.message(F.text, FilmAddStates.kanal)
async def film_quality_add(message: types.Message, state: FSMContext):
    kanal = message.text
    await state.update_data({
        'kanal': kanal
    })
    data = await state.get_data()
    await db.add_channel(data['kanal'])
    await message.answer(f"Yangi kanal qo‘shildi: {kanal}")
    await state.clear()


# Kanal o'chirish
@dp.message(F.text == "M.O kanal o'chrish", IsBotAdmin())
async def delete_channel(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'chirish uchun kanal username'ini kiriting !!!\n\nMisol uchun: @kanal")
    await state.set_state(FilmAddStates.delete_kanal)


@dp.message(F.text, FilmAddStates.delete_kanal)
async def delete_kanal(message: types.Message, state: FSMContext):
    kanal_delete = message.text
    await state.update_data({
        'kanal_delete': kanal_delete
    })
    data = await state.get_data()
    await db.delete_channel(data['kanal_delete'])
    await message.answer(f"Kanal o‘chirildi: {kanal_delete}")
    await state.clear()

# # Majburiy obuna bo'lgan kanallarni ko'rsatish
# @dp.message(Command('list_channels'), IsBotAdmin())
# async def list_channels(message: types.Message):
#     channels = await db.get_all_channels()
#     if channels:
#         channels_text = "\n".join([f"@{channel[0]}" for channel in channels])
#         await message.answer(f"Majburiy kanallar:\n{channels_text}")
#     else:
#         await message.answer("Majburiy kanallar qo'shilmagan.")

#
#
# @dp.message(F.text == "Reklama yuborish", IsBotAdmin())
# async def reklama_start(message: types.Message, state: FSMContext):
#     await message.answer("Reklama yuborish uchun rasm, video yoki matn yuboring.")
#     await state.set_state(FilmAddStates.content)
#
#
# # Matn, rasm yoki videoni qabul qilish
#
#

#
#
# @dp.message(F.text == "🔙 ortga", IsBotAdmin())
# async def start_admin_bot(message: types.Message):
#     await message.answer("🔝 Admin panel....", reply_markup=admin_button())
