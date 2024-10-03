from aiogram import types, F
from aiogram.fsm.context import FSMContext
from loader import dp, db
from keyboards.default.buttons import film_delete_or_join


@dp.message(F.text == "📀 Kino joylash / O'chrish")
async def delete_or_join(message: types.Message, state: FSMContext):
    await message.answer("📀 Kino joylash / O'chrish bo'limi !", reply_markup=film_delete_or_join())


