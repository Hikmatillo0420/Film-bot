from filters import IsBotAdmin
from keyboards.inline.buttons import generate_episode_buttons
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
        await message.answer(f"Serial qismi {episode_number} qo'shildi!\nYana qism qo'shishni xohlaysizmi? (Ha/Yo'q)")
        await state.set_state(FilmAddStates.waiting_for_more_episodes)
    except Exception as e:
        await message.answer("Video qo'shishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        await state.clear()
        logger(str(e))


# Ko'proq qismlar qo'shishni so'rash
@dp.message(FilmAddStates.waiting_for_more_episodes, F.text)
async def more_episodes_decision(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer in ['ha', 'ha!', 'yes', 'y']:
        await message.answer("Serial qismi uchun videoni jo'nating!")
        await state.set_state(FilmAddStates.waiting_for_episode_video)
    elif answer in ['yo\'q', 'no', 'n']:
        data = await state.get_data()
        serial_title = data.get('serial_title')
        serial_banner = data.get('serial_banner')
        episodes = data.get('episodes', [])

        # Serial va qismlar haqida tasdiqlash uchun ma'lumot chiqarish
        serial_title = data.get('serial_title')  # Serial nomini olamiz

        await message.answer_photo(serial_banner, caption=serial_title, reply_markup=generate_episode_buttons(episodes))

        if episodes:
            episodes_list = "\n".join([f"Qism {ep['episode_number']}" for ep in episodes])
            # await message.answer(f"Qismlar:\n{episodes_list}")
        else:
            await message.answer("Qismlar yo'q.")
        await message.answer("Ma'lumotlarni saqlash uchun 'Ha', saqlamaslik uchun 'Yo'q' deb javob bering.")
        await state.set_state(FilmAddStates.waiting_for_confirmation)


# Serial va qismlarni tasdiqlash va bazaga saqlash
@dp.message(FilmAddStates.waiting_for_confirmation, F.text)
async def confirmation_handler(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer in ['ha', 'ha!', 'yes', 'y']:
        data = await state.get_data()
        serial_name = data.get('serial_name')
        serial_banner = data.get('serial_banner')
        serial_title = data.get('serial_title')
        episodes = data.get('episodes', [])

        try:
            # Serialni va qismlarini bazaga qo'shish
            db.add_serial(serial_name, serial_title, serial_banner)
            serial_id = db.get_serial_id(serial_name)

            # Bu yerda serial_id ni state ga saqlab qo'yamiz
            await state.update_data(serial_id=serial_id)

            for ep in episodes:
                db.add_episode(serial_id, ep['episode_number'], ep['video_id'])

            await message.answer_photo(serial_banner, caption="Serial banneri",
                                       reply_markup=generate_episode_buttons(episodes))
            await state.clear()
        except Exception as e:
            await message.answer("Serial va qismlarni saqlashda xatolik yuz berdi.")
            await state.clear()
            logger(str(e))
    elif answer in ['yo\'q', 'no', 'n']:
        await message.answer("Serial va qismlar qo'shilmadi. Jarayon to'xtatildi.")
        await state.clear()



@dp.callback_query(F.data.startswith("view_episode_"))
async def view_episode(callback_query: types.CallbackQuery, state: FSMContext):
    episode_number = int(callback_query.data.split("_")[2])
    await callback_query.answer()

    # State'dan serial_id'ni olish
    data = await state.get_data()
    serial_id = data.get('serial_id')

    if serial_id:
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
    else:
        await callback_query.message.answer("Serial ID aniqlanmadi, iltimos qayta urinib ko'ring.")



@dp.callback_query(F.data.startswith("pagination_"))
async def pagination_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer(cash_time=60)
    page = int(callback_query.data.split("_")[1])

    # FSMContext orqali epizod ma'lumotlarini olish
    data = await state.get_data()
    episodes = data.get('episodes', [])

    if not episodes:
        await callback_query.message.answer("Hozircha epizodlar mavjud emas.")
        return

    # Sahifalangan qismlar ro'yxatini qayta chiqarish
    await callback_query.message.edit_reply_markup(reply_markup=generate_episode_buttons(episodes, page))
