from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN, host, user, password, database
from utils.db_api.mysql import Database
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database(host=host, user=user, password=password, database=database)


# async def is_user_subscribed(user_id: int) -> bool:
#     channels = db.get_all_channels()
#     if not channels:
#         print("Hech qanday kanal mavjud emas.")
#         return True
#     # gg
#
#     for channel in channels:
#         try:
#             chat = await bot.get_chat(chat_id=channel[0])
#             chat_id = chat.id
#             member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
#             if member.status in ['left', 'kicked']:
#                 return False
#         except Exception as e:
#             print(f"Xatolik loader: {e}")
#             return False
#     return True
