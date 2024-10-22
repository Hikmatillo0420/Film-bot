from pydantic.v1.validators import anystr_strip_whitespace

from filters import IsBotAdmin
from keyboards.inline.buttons import generate_episode_buttons, yes_no_button_episode, yes_no_button_confirmation
from loader import dp, db
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.film_add_states import FilmAddStates
from utils.db_api.mysql import logger


@dp.message(F.text == "➕ Serial joylash", IsBotAdmin())
async def serial_add_start(message: types.Message, state: FSMContext):
    await message.answer("Serial kodi!")
    await state.set_state(FilmAddStates.waiting_for_serial_name)


# Serial nomini kiritish
@dp.message(FilmAddStates.waiting_for_serial_name, F.text)
async def serial_name_add(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if db.check_code_exists_serial(name):
        await message.answer("Bu nom allaqachon mavjud. Iltimos, boshqa nom kiriting!")
    else:
        await state.update_data({'serial_name': name, 'episodes': []})
        await message.answer("Serialni haqida :")
        await state.set_state(FilmAddStates.waiting_for_serial_title)


@dp.message(FilmAddStates.waiting_for_serial_title)
async def serial_name_add(message: types.Message, state: FSMContext):
    serial_title = message.text.strip()
    await state.update_data({'serial_title': serial_title})
    await message.answer("Serial banneri uchun rasm jo'nating!")
    await state.set_state(FilmAddStates.waiting_for_serial_banner)


@dp.message(FilmAddStates.waiting_for_serial_banner, F.photo)
async def serial_banner_add(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1]
        file_id = photo.file_id
        await state.update_data({'serial_banner': file_id})
        await message.answer("Serial qismi uchun videoni jo'nating!")
        await state.set_state(FilmAddStates.waiting_for_episode_video)
    except Exception as e:
        await message.answer("Rasmni yuklashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()
        logger(str(e))


# Serial qismi uchun video yuklash
# Serial qismi uchun video yuklash
@dp.message(FilmAddStates.waiting_for_episode_video, F.video)
async def episode_video_add(message: types.Message, state: FSMContext):
    try:
        video = message.video
        video_id = video.file_id  # Video faylning ID sini olamiz
        data = await state.get_data()
        episodes = data.get('episodes', [])
        episode_number = len(episodes) + 1
        episodes.append({'episode_number': episode_number, 'video_id': video_id})  # video_id ni qo'shamiz
        await state.update_data({'episodes': episodes})
        await message.answer(
            f"Serial qismi {episode_number} qo'shildi!\nYana qism qo'shishni xohlaysizmi? (Ha/Yo'q)",
            reply_markup=await yes_no_button_episode()
        )
        await state.set_state(FilmAddStates.waiting_for_more_episodes)
    except Exception as e:
        await message.answer("Video qo'shishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()
        logger(str(e))


# Callback orqali tanlovni boshqarish (Ha/Yo'q)
@dp.callback_query(F.data.in_(['yes_episode', 'no_episode']))
async def more_episodes_decision_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes_episode':
        await callback_query.message.answer("Serial qismi uchun videoni jo'nating!")
        await state.set_state(FilmAddStates.waiting_for_episode_video)
    elif callback_query.data == 'no_episode':
        data = await state.get_data()
        serial_title = data.get('serial_title')
        serial_banner = data.get('serial_banner')
        episodes = data.get('episodes', [])

        # Epizodlarni matn sifatida ko'rsatish yoki rasm bilan
        if episodes:
            episodes_list = "\n".join([f"Qism {ep['episode_number']}" for ep in episodes])
        else:
            await callback_query.message.answer("Qismlar yo'q.")

        await callback_query.message.answer(
            "Ma'lumotlarni saqlash uchun quyidagi tugmalardan birini tanlang:",
            reply_markup=await yes_no_button_confirmation())
        await state.set_state(FilmAddStates.waiting_for_confirmation)

    await callback_query.answer()


# Serial va qismlarni tasdiqlash va bazaga saqlash
@dp.callback_query(FilmAddStates.waiting_for_confirmation, F.data.in_(['confirm_yes', 'confirm_no']))
async def confirmation_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    answer = callback_query.data
    if answer == 'confirm_yes':
        data = await state.get_data()
        serial_name = data.get('serial_name')
        serial_banner = data.get('serial_banner')
        serial_title = data.get('serial_title')
        episodes = data.get('episodes', [])

        try:
            # Serialni va qismlarini bazaga qo'shish
            db.add_serial(serial_name, serial_title, serial_banner)
            serial_id = db.get_serial_id(serial_name)

            # Epizodlarni bazaga qo'shish
            for ep in episodes:
                db.add_episode(serial_id, ep['episode_number'], ep['video_id'])

            # Banner yoki paginationni yubormasdan, faqat tasdiqlovchi xabarni chiqaramiz
            await callback_query.message.answer("Serial va qismlar muvaffaqiyatli saqlandi!")
            await state.clear()
        except Exception as e:
            await callback_query.message.answer("Serial va qismlarni saqlashda xatolik yuz berdi.")
            await state.clear()
            logger(str(e))
    elif answer == 'confirm_no':
        await callback_query.message.answer("Serial qo'shilmadi !")
        await state.clear()

    await callback_query.answer()




@dp.callback_query(F.data.startswith("view_episode_"))
async def view_episode(callback_query: types.CallbackQuery):
    data_parts = callback_query.data.split("_")
    serial_id = int(data_parts[2])  # Because 'view_episode_{serial_id}_{episode_number}'
    episode_number = int(data_parts[3])
    await callback_query.answer()

    # Bazadan epizodlarni olish
    episodes = db.get_episodes_by_serial_id(serial_id)

    # Epizodni topish va video yuborish
    for ep in episodes:
        if ep['episode_number'] == episode_number:
            await callback_query.message.answer_video(video=ep['video_id'],
                                                      caption=f"{episode_number}-qism")
            return

    # Agar epizod topilmasa
    await callback_query.message.answer("Epizod topilmadi.")


@dp.callback_query(F.data.startswith("pagination_"))
async def pagination_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data_parts = callback_query.data.split("_")
    serial_id = int(data_parts[1])
    page = int(data_parts[2])
    # Bazadan epizodlarni olish
    episodes = db.get_episodes_by_serial_id(serial_id)
    if not episodes:
        await callback_query.message.answer("Hozircha epizodlar mavjud emas.")
        return

    # Sahifalangan qismlar ro'yxatini qayta chiqarish
    await callback_query.message.edit_reply_markup(reply_markup=generate_episode_buttons(episodes, serial_id, page))
