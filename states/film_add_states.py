from aiogram.filters.state import State, StatesGroup


class FilmAddStates(StatesGroup):
    kod = State()
    kod_2 = State()
    chekk = State()
    film_id = State()
    content = State()
    ask_ad_content = State()
    file_name = State()
    check_kanal = State()
    waiting_for_channel_link=State()
