from aiogram.filters.state import State, StatesGroup


class FilmAddStates(StatesGroup):
    kod = State()
    kod_2 = State()
    chekk = State()
    film_id = State()
    film_name = State()
    content = State()
    ask_ad_content = State()
    file_name = State()
    check_kanal = State()
    waiting_for_channel_link=State()
    chat_id = State()
    admin_chat_id = State()
    waiting_for_serial_name = State()
    waiting_for_part_title = State()
    waiting_for_next_action = State()

    # Serial qidirish holatlari
    waiting_for_serial_search = State()
    waiting_for_serial_selection = State()
    serial_view = State()
    waiting_for_serial_image =State()
    waiting_for_episode =State()
    waiting_for_confirmation =State()
