from aiogram.types import CallbackQuery, InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from keyboards.default.buttons import admin_button
from keyboards.inline.buttons import yes_no_button
from loader import dp, bot, db, is_user_subscribed
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates


@dp.message(F.text == "Kino joylash")
async def film_name_add(message: types.Message, state: FSMContext):
    await message.answer("🎥Kino nomi : ")
    await state.set_state(FilmAddStates.name)


@dp.message(F.text, FilmAddStates.name)
async def film_quality_add(message: types.Message, state: FSMContext):
    await message.answer("⚙️Kino sifati : ")
    await state.set_state(FilmAddStates.quality)
    name = message.text
    await state.update_data({
        'name': name
    })


@dp.message(F.text, FilmAddStates.quality)
async def film_quality_add(message: types.Message, state: FSMContext):
    await message.answer("📃Kino tili : ")
    await state.set_state(FilmAddStates.language)
    quality = message.text
    await state.update_data({
        'quality': quality
    })


@dp.message(F.text, FilmAddStates.language)
async def film_quality_add(message: types.Message, state: FSMContext):
    await message.answer("📁Kino tagi : ")
    await state.set_state(FilmAddStates.resource)
    language = message.text
    await state.update_data({
        'language': language
    })


@dp.message(F.text, FilmAddStates.resource)
async def film_quality_add(message: types.Message, state: FSMContext):
    await message.answer("Filmni yuboring !")
    await state.set_state(FilmAddStates.film)
    resource = message.text
    await state.update_data({
        'resource': resource
    })


@dp.message(FilmAddStates.film)
async def get_video_file_id(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    await state.update_data({
        'film': file_id
    })

    data = await state.get_data()
    text = (
        f" 🎥Kinoni nomi : {data['name']}\n\n"
        f" ⚙️Sifati: {data['quality']}\n\n"
        f" 📃Tili: {data['language']}\n\n"
        f" 📁Manba: {data['resource']}\n\n"
        f" 📍Bizning bot: @MeshpolvonFilm_bot"
    )

    await message.answer("Barcha ma'lumotlar to'g'rimi?")
    await message.answer_video(file_id)
    await message.answer(text=text, reply_markup=await yes_no_button(), parse_mode="HTML")

    await state.set_state(FilmAddStates.chekk)


@dp.callback_query(F.data == 'yes', FilmAddStates.chekk)
async def get_check_1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.add_film(data['name'], data['quality'], data['language'], data['resource'], data['film'])

    await call.message.answer("Ma'lumotlari qabul qilindi\n")
    await call.message.delete()
    await state.clear()


@dp.callback_query(F.data == 'no', FilmAddStates.chekk)
async def get_check_0(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Kiritilgan ma'lumotlar o'chirib tashlandi !", reply_markup=admin_button())
    await call.message.delete()
    await state.clear()


async def echo_message(message: types.Message):
    await message.answer(f"{message.text} - id bilan hech qanday kino topilmadi ❌")

@dp.message(F.text)
async def return_film_by_id(message: types.Message):
    user_id = message.from_user.id

    if str(user_id) not in ADMINS:
        if not await is_user_subscribed(user_id):
            channels = await db.get_all_channels()
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=f" {channel[0]}", url=f"https://t.me/{channel[0][1:]}")]
                    for channel in channels
                ]
            )
            await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling va qayta urinib ko‘ring:", reply_markup=keyboard)
            return
    try:
        film_id = int(message.text.strip())
    except ValueError:
        await message.answer("Iltimos, to'g'ri ID raqamini kiriting.")
        return
    row = await db.get_film_by_id(film_id)
    if row:
        text = (
            f"⌨️ ID: #{row[0]}\n\n"  # row[0] - ID 
            f"🎥 Kinoni nomi : {row[1]}\n\n"  # row[1] - name 
            f"⚙️ Sifati: {row[2]}\n\n"
            f"📃 Tili: {row[3]}\n\n"
            f"📁 Manba: {row[4]}\n\n"
            f"📍 Bizning bot: @MeshpolvonFilm_bot"
        )
        await message.answer_video(row[5], caption=text, parse_mode="HTML")  # row[5] - file_id
    else:
        await echo_message(message)