from aiogram import Bot
from data.config import ADMINS
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish // Запустить бота // Start the bot"),
        BotCommand(command="/help", description="Yordam // Помощь // Help"),
    ]

    admin_commands = [
        BotCommand(command="/chp", description="Parol yangilash"),
        BotCommand(command="/allusers", description="Hamma foydalanuvchilar ro'yxati"),
        BotCommand(command="/cleandb", description="Bazani to'liq bo'shatish"),
    ]

    # if 

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=admin_commands, scope=ADMINS)


# async def admin_commands(bot: Bot):
#     commands = [
#         BotCommand(command="/chp", description="Parol yangilash"),
#         BotCommand(command="/allusers", description="Hamma foydalanuvchilar ro'yxati"),
#         BotCommand(command="/cleandb", description="Bazani to'liq bo'shatish"),
#     ]

#     await bot.set_my_commands(commands=commands, scope=ADMINS)
