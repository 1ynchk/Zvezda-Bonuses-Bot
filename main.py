from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv
import os
import asyncio

from Common.pagination import pagination_router
from Commands.MainCommands import mainCommands
from Callbacks.AdminCallbacks.admin import AdminCallbackRouter
from Callbacks.ModeratorCallbacks.moderator import ModeratorRouter

from Data.types.core import create_tables

load_dotenv()

class TelegramBot:

    def __init__(self, bot, dp):
        self.bot = bot 
        self.dp = dp 
        self.dp.include_routers(
            ModeratorRouter,
            pagination_router,
            mainCommands,
            AdminCallbackRouter,
        )

async def on_startup(bot):
    return await bot.set_my_commands(
        commands=[
            types.BotCommand(description='Панель модератора 🧑‍🔧', command='/moderator'),
            types.BotCommand(description='Панель админа 👨‍💻', command='/admin'),
        ]
    )

async def main():
    BOT = Bot(os.getenv('TOKEN'))
    DP = Dispatcher()
    start_bot = TelegramBot(BOT, DP)
    await on_startup(BOT)
    await DP.start_polling(BOT, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
