from filters import IsBotAdmin
from loader import dp, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates

@dp.message(F.text == "➕ Serial joylash", IsBotAdmin())
async def film_name_add(message: types.Message, state: FSMContext):
    await message.answer("Serial kodini yuboring!")
    await state.set_state(FilmAddStates.waiting_for_serial_id)
