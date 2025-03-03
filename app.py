from loader import dp, bot, db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio

from middlewares.subscription_middleware import UserCheckMiddleware
from utils.notify_admins import start, shutdown
from utils.set_botcommands import commands
# Info
import logging
import sys


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        # await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        dp.update.outer_middleware(UserCheckMiddleware())
        # Create Users Table
        try:
            db.create_table_admins()
        except Exception as e:
            print(e)
        try:
            db.create_table_users()
        except Exception as e:
            print(e)

        try:
            db.create_table_kanal()
        except Exception as e:
            print(e)

        try:
            db.create_table_data()
        except Exception as e:
            print(e)

        try:
            db.create_table_admins()
        except Exception as e:
            print(e)

        try:
            db.create_table_serials()
        except Exception as e:
            print(e)

        try:
            db.create_table_episodes()
        except Exception as e:
            print(e)


        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
