from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def admin_button():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Reklama yuborish"), KeyboardButton(text="🛎 Obunachilar soni")],
            [KeyboardButton(text="📀 Kino joylash / O'chrish"), KeyboardButton(text="📌Majburiy Obuna")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button


def majburiy_obuna():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kanal qo'shish"), KeyboardButton(text="➖ Kanal o'chrish")],
            [KeyboardButton(text="👁‍🗨 Majburiy kanallarni ko'rish"), KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button


def film_delete_or_join():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Kino joylash"), KeyboardButton(text="➖ Kino o'chrish")],
            [KeyboardButton(text="🔝 Asosiy admin panel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return button
