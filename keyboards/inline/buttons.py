from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def yes_no_button():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ha", callback_data="yes"),
             InlineKeyboardButton(text="Yo'q", callback_data="no")]]

    )
    return button


async def yes_no_button_2():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ha", callback_data="yeah"),
             InlineKeyboardButton(text="Yo'q", callback_data="noo")]]

    )
    return button


async def subscription_button():
    channels = db.get_all_channels()  # channels: [{'chat_id': '-1001562032753', 'url': 'https://t.me/...'}, ...]
    inline_keyboard = []

    for sanoq, channel in enumerate(channels, start=1):
        button = InlineKeyboardButton(text=f"{sanoq} - kanal", url=channel['url'])
        inline_keyboard.append([button])

    inline_keyboard.append([
        InlineKeyboardButton(text="Obuna bo'ldim✅", callback_data="subscribe_true")  # callback_data qisqa va aniq
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def delete_channel_button():
    kanallar = db.get_all_channels()
    inline_keyboard = []

    for kanal in kanallar:
        tugma = InlineKeyboardButton(
            text=f"{kanal['url']}",
            callback_data=f"delete_channel_{kanal['chat_id']}"
        )
        inline_keyboard.append([tugma])



    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def delete_admin_button():
    adminlar = db.get_all_admins()  # Barcha adminlarni olish
    inline_keyboard = []

    for admin in adminlar:
        tugma = InlineKeyboardButton(
            text=f"{admin['user_name']}",  # Adminning user_name'ini ko'rsatish
            callback_data=f"delete_admin_{admin['user_id']}"  # Callback uchun user_id ni ishlatish
        )
        inline_keyboard.append([tugma])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

