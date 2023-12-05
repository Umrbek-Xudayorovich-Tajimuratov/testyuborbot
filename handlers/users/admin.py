import logging
import asyncio
import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import db, bot
from keyboards.inline.buttons import are_you_sure_markup
from states.change_P import ChangePassword
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.password_generator import generate_password
from utils.pgtoexcel import export_to_excel

router = Router()


@router.message(Command('allusers'), IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    users = db.select_all_users() 
    file_path = f"documents/users_list.xlsx"
    await export_to_excel(data=users, headings=['HEMIS ID', 'PAROL','TELEGRAM ID', 'FIO','KAFEDRA','LAVOZIM', 'TELEFON', 'TIL'], filepath=file_path)

    await message.answer_document(types.input_file.FSInputFile(file_path))


# todo: change password of teacher by admin
@router.message(Command('chp'), IsBotAdminFilter(ADMINS))
async def get_hemis_ID(message: types.Message, state: FSMContext):
    await message.answer("Hemis_ID kiriting!")
    current_state = await state.get_state()
    await state.update_data(current_state=current_state)
    await state.set_state(ChangePassword.chp)

@router.message(ChangePassword.chp, IsBotAdminFilter(ADMINS))
async def change_password(message: types.Message,state: FSMContext):
    new_password = generate_password()
    admins_hemis_id = message.text.strip()
    data = await state.get_data()
    prev_state = data.get('current_state')

    user_exists = db.check_user_exists(hemis_id=[admins_hemis_id])
    if user_exists[0]!=0:   
        # Enter the user's new password into the database
        try:
            db.update_user_password(hemis_id=admins_hemis_id,password=new_password )
        except sqlite3.IntegrityError as err:
            logging.info(f"Error: {err}")

        await message.answer(f"<b>HEMIS_ID:</b> <code>{admins_hemis_id}</code>\n<b>PAROL:</b> <code>{new_password}</code>\n\n<i>Parol muvaffaqiyatli o'zgartirildi.</i>")
    else:
        await message.answer(f"/chp\nQayta urinib ko'ring!\n<b>Xatoliklar:</b>\n<code>1.Siz hemis ID ni xato kiritdingiz!\n2.HEMIS ID bazada yo'q!</code>")

    # Change state to groups
    await state.set_state(prev_state)
# todo: END change password of teacher by admin-----

@router.message(Command('reklama'), IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)

    
@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    count = 0
    for user in users:
        user_id = user[-1]
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
    await state.clear()


@router.message(Command('cleandb'), IsBotAdminFilter(ADMINS))
async def ask_are_you_sure(message: types.Message, state: FSMContext):
    msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?", reply_markup=are_you_sure_markup)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.are_you_sure)


@router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(ADMINS))
async def clean_db(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    if call.data == 'yes':
        db.delete_users()
        text = "Baza tozalandi!"
    elif call.data == 'no':
        text = "Bekor qilindi."
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    await state.clear()
