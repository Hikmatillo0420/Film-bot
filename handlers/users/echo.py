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
        text = (
            f"⌨️ KOD: #{row['kod']}\n\n"  # row[0] - ID
            f" 📍Bizning bot: @kmfilmlar_bot"
            # f"🎥 Kino yili : {row['all']}\n\n"  # row[1] - name
        )
        await message.answer_video(row['file_id'], caption=text, parse_mode="HTML")  # row[5] - file_id
    else:
        await echo_message(message)
