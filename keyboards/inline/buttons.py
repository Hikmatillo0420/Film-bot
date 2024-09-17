from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def yes_no_button():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ha", callback_data="yes"),
             InlineKeyboardButton(text="Yo'q", callback_data="no")]]

    )
    return button


async def subscription_button():
    channels = await db.get_all_channels()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{channel[0]}", url=f"https://t.me/{channel[0][1:]}")]
            for channel in channels
        ]
    )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")]
    )
    return keyboard
