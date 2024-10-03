from aiogram.types import CallbackQuery

from filters import IsBotAdmin
from keyboards.default.buttons import admin_button
from keyboards.inline.buttons import yes_no_button
from loader import dp, bot, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates
from aiogram.types import ReplyKeyboardRemove


@dp.message(F.text == "➕ Kino joylash", IsBotAdmin())
async def film_name_add(message: types.Message, state: FSMContext):
    await message.answer("Filmni kodini yuboring!")
    await state.set_state(FilmAddStates.kod)


@dp.message(F.text, FilmAddStates.kod)
async def film_check_code(message: types.Message, state: FSMContext):
    kod = message.text
    if db.check_code_exists(kod):
        await message.answer("Bu kod allaqachon mavjud. Iltimos, boshqa kod kiriting!")
    else:
        await state.update_data({'kod': kod})
        await message.answer("Filmni yuboring:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(FilmAddStates.film_id)


@dp.message(FilmAddStates.film_id)
async def get_video_file_id(message: types.Message, state: FSMContext):
    film_id = message.video.file_id
    file_name = message.video.file_name
    if file_name is None:
        file_name = 'gg'
    await state.update_data({
        'film_id': film_id,
        'file_name': file_name
    })
    data = await state.get_data()
    text = (
        f"⌨️ KOD: #{data['kod']}\n\n"
    )

    await message.answer("Barcha ma'lumotlar to'g'rimi ?")
    await message.answer_video(film_id)
    await message.answer(text=text, reply_markup=await yes_no_button(), parse_mode="HTML")

    await state.set_state(FilmAddStates.chekk)


@dp.callback_query(F.data == 'yes', FilmAddStates.chekk)
async def get_check_1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    all_data = 1
    print(data)
    db.add_film_data(data['file_name'], data['film_id'], data['kod'], all_data)

    await call.message.answer("Ma'lumotlari qabul qilindi\n")
    await call.message.delete()
    await state.clear()


@dp.callback_query(F.data == 'no', FilmAddStates.chekk)
async def get_check_0(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Kiritilgan ma'lumotlar o'chirib tashlandi !", reply_markup=admin_button())
    await call.message.delete()
    await state.clear()

#
# async def echo_message(message: types.Message):
#     await message.answer(f"{message.text} - id bilan hech qanday kino topilmadi ❌")
#
#
# @dp.message(F.text)
# async def return_film_by_id(message: types.Message):
#     try:
#         film_id = int(message.text.strip())
#     except ValueError:
#         await message.answer("Iltimos, to'g'ri ID raqamini kiriting.")
#         return
#     row = db.get_film_by_id(film_id)
#     if row:
#         text = (
#             f"⌨️ KOD: #{row['kod']}\n\n"  # row[0] - ID
#             f" 📍Bizning bot: @kmfilmlar_bot"
#             # f"🎥 Kino yili : {row['all']}\n\n"  # row[1] - name
#         )
#         await message.answer_video(row['file_id'], caption=text, parse_mode="HTML")  # row[5] - file_id
#     else:
#         await echo_message(message)
