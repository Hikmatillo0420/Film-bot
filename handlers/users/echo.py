from aiogram import F, types

from loader import dp, db


async def echo_message(message: types.Message):
    await message.answer(f"{message.text} - id bilan hech qanday kino topilmadi ❌")


@dp.message(F.text)
async def return_film_by_id(message: types.Message):
    try:
        film_id = int(message.text.strip())
    except ValueError:
        await message.answer("Iltimos, to'g'ri ID raqamini kiriting.")
        return

    row = db.get_film_by_id(film_id)

    if row:
        name_film = db.get_film_by_name(film_id)  # Pass film_id to get_film_by_name
        text = (
            f"⌨️ KOD: #{row['kod']}\n"
            f"📑 Name: {name_film['file_name']}\n\n"  # Use the correct field name here
            f" 📍Bizning bot: @kmfilmlar_bot"
        )
        await message.answer_video(row['file_id'], caption=text, parse_mode="HTML")  # row['file_id'] is correct
    else:
        await echo_message(message)

