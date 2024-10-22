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
    waiting_for_serial_banner = State()
    waiting_for_episode_number = State()
    waiting_for_episode_name = State()
    waiting_for_more_episodes = State()
    waiting_for_episode_video = State()
    waiting_for_confirmation = State()
    waiting_for_serial_title = State()
    waiting_for_serial_delete  = State()

