from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv
import os
import asyncio

from Common.pagination import pagination_router
from Commands.MainCommands import mainCommands
from Callbacks.AdminCallbacks.admin import AdminCallbackRouter
from Callbacks.ModeratorCallbacks.moderator import ModeratorRouter

load_dotenv()

BOT = Bot(os.getenv('TOKEN'))
DP = Dispatcher()

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

async def keep_alive(dispatcher):
    print('hello')
    while True:
        try:
            await dispatcher.bot.get_me()
        except Exception as e:
            print(f"Connection lost: {e}")
        await asyncio.sleep(600)

async def main():
    start_bot = TelegramBot(BOT, DP)
    await on_startup(BOT)
    await DP.start_polling(BOT, skip_updates=True)

async def start():
    await asyncio.gather(
        main(),
        keep_alive(DP)
    )

if __name__ == '__main__':
    asyncio.run(start())
