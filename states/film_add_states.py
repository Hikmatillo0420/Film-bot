from aiogram.filters.state import State, StatesGroup


class FilmAddStates(StatesGroup):
    name = State()
    quality = State()
    language = State()
    resource = State()
    chekk = State()
    film = State()
    kanal = State()
    delete_kanal = State()
    content = State()
    ask_ad_content = State()
