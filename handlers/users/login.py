import json
import logging
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.user_login import UserData
from states.test_states import SendTest
from loader import db, bot,router
from data.config import ADMINS, CHANNEL_ID
from keyboards.reply.back import back_en,back_uz,back_ru
import sqlite3
import re
from utils.delete_message import delete_message
# from utils.delete_message import delete_all_messages
from utils.hemis_api import hemis_api_call
from utils.password_generator import generate_password


@router.message(UserData.hemis_id)
async def add_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')
    hemis_id =message.text.strip()
    
    chat_id = message.chat.id
    message_id = message.message_id
    # Delete the messages
    await delete_message(chat_id=chat_id,message_id=message_id)
    
    # we do not accept if anything other than hemis_id number is written
    if bool(re.match(r"^\d{8,}$", hemis_id)):

        # import teacher data from HEMIS API
        data = hemis_api_call(hemis_id=hemis_id)
        # If the teacher is not in the database, the list with an error 
        # will be returned. If true, object
        if not isinstance(data, list):

            # Update the state machine's data with the chosen datas
            await state.update_data(
                {
                    "hemis_id":         hemis_id,
                    "name":             data['name'],
                    "department":       data['department'],
                    "staff_position":   data['staff_position'],
                })
            
            user_exists = db.check_user_exists(hemis_id=[int(hemis_id)])
            if not user_exists[0]:
                new_password = generate_password()
                # Enter the user into the database
                try:
                    db.add_user(hemis_id=int(hemis_id),
                                password=new_password,
                                user_id=message.from_user.id,
                                name=data['name'],
                                department=data['department'],
                                staff_position=data['staff_position'],
                                language=bot_language)
                except sqlite3.IntegrityError as err:
                    logging.info(f"Error: {err}")

                msg = f"<b>USERNAME:</b> @{message.from_user.username}\n<b>USER_LINK:</b> {message.from_user.url}\n\n<b>NAME:</b> <code>{data['name']}</code>\n<b>HEMIS_ID:</b> <code>{hemis_id}</code>\n<b>PASSWORD:</b> <code>{new_password}</code>\n\n<i>User muvaffaqiyatli qo'shildi.</i>\n#new_user"
                await bot.send_message(chat_id=CHANNEL_ID[0], text=msg)

            if bot_language=='uz':
                await message.answer(f"🔐 Parolni kiriting\n",reply_markup=back_uz)
            elif bot_language=='ru':
                await message.answer(f"🔐 Введите пароль\n",reply_markup=back_ru)
            elif bot_language=='en':
                await message.answer(f"🔐 Enter the Password\n",reply_markup=back_en)

            # Change state to hemis_password
            await state.set_state(UserData.hemis_password)

        else:
            if bot_language == 'uz':
                await message.answer(f"{data[0]['error_uz']}")
            elif bot_language == 'ru':
                await message.answer(f"{data[0]['error_ru']}")
            elif bot_language == 'en':
                await message.answer(f"{data[0]['error_en']}")
    else:
        if bot_language=='uz':
            await message.answer(
            f'''HEMIS_ID faqat 8+ sondan iborat bo'lishi kerak\nQayta urining''')
        elif bot_language=='ru':
            await message.answer(
            f'''HEMIS_ID должен быть только 8+ числовым\nПожалуйста, повторите попытку.''')
        elif bot_language=='en':
            await message.answer(
            f'''HEMIS_ID must be 8+ numeric only\nPlease try again''')



@router.message(UserData.hemis_password)
async def add_user(message: types.Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()
    hemis_id = data.get('hemis_id')
    bot_language = data.get('bot_lang')

    chat_id = message.chat.id
    message_id = message.message_id
    # Delete the messages
    await delete_message(chat_id=chat_id,message_id=message_id)
    
    
    user_exists = db.check_user_password(hemis_id=int(hemis_id), password=password)
    # we do not accept if anything other than password  is written
    if bool(re.match(r"^[a-z]\d{5}$", password)) and (user_exists[0]!=0):

        teacher_name = data.get("name")
        department = json.loads(data.get('department'))
        staff_position = json.loads(data.get('staff_position'))

        dep_staf = ''
        for index in range(len(department)):
            if bot_language == 'uz':
                dep_staf += f"<b>⛺️ KAFEDRA{index+1}:</b> <code>{department[index]}</code>\n<b>🧰 LAVOZIM{index+1}:</b> {staff_position[index]}\n"
            elif bot_language == 'ru':
                dep_staf += f"<b>⛺️ ОТДЕЛ{index+1}:</b> <code>{department[index]}</code>\n<b>🧰 ДОЛЖНОСТЬ{index+1}:</b> {staff_position[index]}\n"
            elif bot_language == 'en':
                dep_staf += f"<b>⛺️ DEPARTMENT{index+1}:</b> <code>{department[index]}</code>\n<b>🧰 POSITION{index+1}:</b> {staff_position[index]}\n"

        # Update the state machine's data with the chosen datas
        await state.update_data(
            {
                "password": password,
            })
        
        # chat_id = message.chat.id
        # chat_type = message.chat.type
        # # Delete the messages
        # await delete_all_messages(chat_id, chat_type)

        if bot_language == 'uz':
            btn = back_uz
            msg = f"🪪 <b>TEST JO'NATUVCHI:</b>\n\n<i><b>👨‍🏫 FIO:</b></i> <code>{teacher_name}</code>\n<i><b>🆔 HEMIS_ID:</b></i> <code>{hemis_id}</code>\n{dep_staf}\n\n"
            msg_one = "<i>Jo'natmoqchi bo'lgan test (.txt) faylini yuklang</i>"
        elif bot_language == 'ru':
            btn = back_ru
            msg = f"🪪 <b>ОТПРАВИТЕЛЬ ТЕСТА:</b>\n\n<i><b>👨‍🏫 ФИО:</b></i> <code>{teacher_name}</code>\n<i><b>🆔 HEMIS_ID:</b></i> <code>{hemis_id}</code>\n{dep_staf}\n\n"
            msg_one = "<i>Загрузите тестовый файл (.txt), который хотите отправить</i>"
        elif bot_language == 'en':
            btn = back_en
            msg = f"🪪 <b>TEST SENDER:</b>\n\n<i><b>👨‍🏫 NAME:</b></i> <code>{teacher_name}</code>\n<i><b>HEMIS_ID:</b></i> <code>{hemis_id}</code>\ n{dep_staf}\n\n"
            msg_one = "<i>Upload the test (.txt) file you want to send</i>"
            
        await message.answer(f"<blockquote>{msg}</blockquote>\n\n📥{msg_one}",reply_markup=btn)
        # await message.answer(msg_one)

        # Change state to hemis_password
        await state.set_state(SendTest.test_file)

    else:
        if bot_language == 'uz':
            await message.answer(
                f'''<b>🚫 PAROL XATO!</b>\nQayta urining''')
        elif bot_language == 'ru':
            await message.answer(
                f'''<b>🚫 ОШИБКА ПАРОЛЯ!</b>\nПожалуйста, повторите попытку.''')
        elif bot_language == 'en':
            await message.answer(
                f'''<b>🚫 PASSWORD ERROR!</b>\nPlease try again''')
