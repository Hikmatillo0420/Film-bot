from aiogram.fsm.context import FSMContext

from filters import IsBotAdmin
from loader import dp, db
from aiogram import types, F

from states.film_add_states import FilmAddStates
from keyboards.default.buttons import admin_button


@dp.message(F.text == "🔙 Orqaga", IsBotAdmin())
async def orqaga(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔝 Asosiy Menyu", reply_markup=admin_button())


@dp.message(F.text == "➕ Kanal qo'shish", IsBotAdmin())
async def add_channel(message: types.Message, state: FSMContext):
    await message.answer("Telegram kanal username'ini kiriting !!!\n\nMisol uchun: @kanal ")
    await state.set_state(FilmAddStates.kanal)


@dp.message(F.text, FilmAddStates.kanal)
async def film_quality_add(message: types.Message, state: FSMContext):
    kanal = message.text

    if not kanal.startswith('@') or ' ' in kanal:
        await message.answer("Iltimos, to'g'ri formatda kanal username'ini kiriting! Misol uchun: @kanal")
        return

    await state.update_data({
        'kanal': kanal
    })
    data = await state.get_data()
    await db.add_channel(data['kanal'])
    await message.answer(f"Yangi kanal qo‘shildi: {kanal}")
    await state.clear()


@dp.message(F.text == "➖ Kanal o'chrish", IsBotAdmin())
async def delete_channel(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, o'chirish uchun kanal username'ini kiriting !!!\n\nMisol uchun: @kanal")
    await state.set_state(FilmAddStates.delete_kanal)


@dp.message(F.text, FilmAddStates.delete_kanal)
async def delete_kanal(message: types.Message, state: FSMContext):
    kanal_delete = message.text

    if not kanal_delete.startswith('@') or ' ' in kanal_delete:
        await message.answer("Iltimos, to'g'ri formatda kanal username'ini kiriting! Misol uchun: @kanal")
        return

    await state.update_data({
        'kanal_delete': kanal_delete
    })
    data = await state.get_data()
    await db.delete_channel(data['kanal_delete'])
    await message.answer(f"Kanal o‘chirildi: {kanal_delete}")
    await state.clear()


@dp.message(F.text == "👁‍🗨 Majburiy kanallarni ko'rish", IsBotAdmin())
async def list_channels(message: types.Message):
    channels = await db.get_all_channels()
    if channels:
        channels_text = "\n".join([f"{channel[0]}" for channel in channels])
        await message.answer(f"Majburiy kanallar:\n\n{channels_text}")
    else:
        await message.answer("Majburiy kanallar qo'shilmagan.")
