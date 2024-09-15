from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
def admin_button():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Reklama yuborish"), KeyboardButton(text="Obunachilar soni")],
            [KeyboardButton(text="Kino joylash"), KeyboardButton(text="M.O kanal qo'shish")],
            [KeyboardButton(text="M.O kanal o'chrish"), KeyboardButton(text="M.O kanallar")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button