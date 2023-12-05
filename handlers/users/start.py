# from aiogram.client.session.middlewares.request_logging import logger
# from aiogram.enums.parse_mode import ParseMode
# from utils.extra_datas import make_title
# from data.config import ADMINS
import asyncio
from aiogram import  types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.inline.lang_menuKB import lang_menu
from states.home import HomeState
from states.languages import Language
from utils.delete_message import delete_message
from loader import router


@router.message(CommandStart())
@router.message(F.text.in_ ({"🌏 Tilni o'zgartirish","🌏 Изменить язык","🌏 Changing language"}))
async def do_start(message: types.Message, state: FSMContext):
        
    ans_mes = await message.answer(
        f'''Salom (Hi, Привет), <b>{message.from_user.full_name}</b>!
        Xush kelibsiz! Welcome! Добро пожаловать!
        ***
        🇺🇿 Tilni tanlang
        🇷🇺 Выберите язык
        🇬🇧 Choose language''', reply_markup=lang_menu)
    await asyncio.sleep(0.5)

    await state.update_data(
        {
            "del_msg": ans_mes
        }
    )

    # await delete_message(chat_id=chat_id, message_id=message_id)
    await state.set_state(HomeState.home_state)
    # await state.set_state(Language.language)




    # telegram_id = message.from_user.id
    # full_name = message.from_user.full_name
    # username = message.from_user.username
    # user = None
    # try:
    #     user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    # except Exception as error:
    #     logger.info(error)
    # if user:
    #     count = await db.count_users()
    #     msg = (f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    # else:
    #     msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
    # for admin in ADMINS:
    #     try:
    #         await bot.send_message(
    #             chat_id=admin,
    #             text=msg,
    #             parse_mode=ParseMode.MARKDOWN_V2
    #         )
    #     except Exception as error:
    #         logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    # await message.answer(f"Assalomu alaykum {make_title(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2)
