import json
import logging
import os
import sqlite3
from aiogram import types, F
from keyboards.reply.phone_sendingKB import phone_uz, phone_en, phone_ru
from keyboards.reply.back import back_en,back_uz,back_ru
from states.test_states import SendTest
from aiogram.fsm.context import FSMContext
from data.config import ADMINS, CHANNEL_ID

from loader import router, bot, db
from states.user_login import UserData
from keyboards.inline.buttons import are_you_sure_markup

from utils.check_test_file import check_tests, check_utf
# from utils.delete_message import delete_all_messages
from utils.valid_phone_number import valid_phone


# Define a function to handle incoming files
@router.message(F.content_type == 'document', SendTest.test_file)
async def handle_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')

    given_file = message.document


    if given_file.mime_type=='text/plain':

        # Get the document ID from the user
        file_id = message.document.file_id

        fi = await bot.get_file(file_id)
        file_path = fi.file_path

        # Update the state machine's data with the chosen data
        await state.update_data(
            {
                "file_id": file_id
            }
        )

        # Check the file is in utf-8 format or not
        is_utf_8 = await check_utf(given_file=given_file, file_path=file_path)
        if is_utf_8:            
            errors=''
            errs = await check_tests(file_path, bot_language)
            if len(errs)!=0:
                for e in errs:  
                    errors+= f"{e['index']}.{e['definition']}\n"
                await message.reply(f"<pre>{errors}</pre>")
                
            else:
                # chat_id = message.chat.id
                # Delete the message
                # await delete_all_messages(chat_id)

                if bot_language=="uz":
                    await message.reply("<blockquote>✅ Faylingiz xatosiz! Muvafaqqiyatli qabul qilindi</blockquote>\n\n<i>Test topshiradigan guruhlarni yozing</i>",reply_markup=back_uz)
                elif bot_language=="en":
                    await message.reply("<blockquote>✅ Your file is error free! Accepted successfully</blockquote>\n\n<i>Type the groups which the test will be taken</i>",reply_markup=back_en)
                elif bot_language=="ru":
                    await message.reply("<blockquote>✅ Ваш файл без ошибок! Принято успешно</blockquote>\n\n<i>Укажите группы, для которых будет проводиться тест</i>",reply_markup=back_ru)
                
                # Change state to groups
                await state.set_state(SendTest.groups)
        else:
            if bot_language=="uz":
                await message.reply("✖️ Fayl <i><b>UTF-8</b></i> formatida kodlanmagan")
            elif bot_language=="en":
                await message.reply("✖️ The file is not encoded in <i><b>UTF-8</b></i> format")
            elif bot_language=="ru":
                await message.reply("✖️ Файл не закодирован в формате <i><b>UTF-8</b></i>.")
            
        os.remove(file_path)

    else:
        if bot_language=='uz':
            await message.answer("⚠️ Iltimos menga .txt file jo'nating!\n Word, Excel, PDF, emoji, gif, stiker, foto va video fayl qabul qilinmaydi!")
        elif bot_language=='ru':
            await message.answer("⚠️ Пожалуйста, пришлите мне файл .txt!\n Файлы Word, Excel, PDF, смайлики, гифки, стикеры, фото и видео не принимаются!")
        elif bot_language=='en':
            await message.answer("⚠️ Please send me a .txt file!\n Word, Excel, PDF, emoji, gif, sticker, photo and video files are not accepted!")


# Define a function to handle incoming not file
# {'photo', 'animation', 'sticker', 'video', 'audio','text'}
@router.message(F.content_type.not_in({'document'}), SendTest.test_file)
async def err_doc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')

    if bot_language=='uz':
        await message.answer("⚠️ Iltimos menga .txt file jo'nating!\n Emoji, gif, stiker, foto va video fayl qabul qilinmaydi!")
    elif bot_language=='ru':
        await message.answer("⚠️ Пожалуйста, пришлите мне файл .txt!\n Смайлики, гифки, стикеры, фото и видео не принимаются!")
    elif bot_language=='en':
        await message.answer("⚠️ Please send me a .txt file!\n Emoji, gif, sticker, photo and video files are not accepted!")


# Define a function to handle incoming groups
@router.message(SendTest.groups)
async def handle_groups(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')
    groups = message.text.strip()
    # Update the state machine's data with the chosen data
    await state.update_data(
        {
            "groups": groups
        }
    )
    # chat_id = message.chat.id
    # # Delete the message
    # await delete_all_messages(chat_id)
    
    if bot_language=='uz':
        await message.answer("<blockquote>✅ Test topshiradigan guruhlar qabul qilindi</blockquote>\n\n<i>Fan nomini o'zbekcha yozing</i>")
    elif bot_language=='ru':
        await message.answer("<blockquote>✅ Принимаются тестовые группы</blockquote>\n\n<i>Напишите название предмета на узбекском языке</i>")
    elif bot_language=='en':
        await message.answer("<blockquote>✅ Test groups accepted</blockquote>\n\n<i>Write the name of the subject in Uzbek</i>")

    # Change state to groups
    await state.set_state(SendTest.subject)



# Define a function to handle incoming subject
@router.message(SendTest.subject)
async def handle_subject(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')
    subject = message.text.strip()
    # Update the state machine's data with the chosen data
    await state.update_data(
        {
            "subject": subject
        }
    )

    # chat_id = message.chat.id
    # # Delete the message
    # await delete_all_messages(chat_id)
    
    if bot_language=='uz':
        await message.answer("<blockquote>✅ Test topshiradigan Fan qabul qilindi</blockquote>\n\n<i>Telefon raqamini kiriting.</i>\n+998 90 123 45 67\n<b>Telefon raqamini yozish orqali</b>\n<code>1. Testning mantiqiy tuzilishi xatolardan holi ekanini tasdiqlagan bo'lasiz.\n2. Avtomatik Kafolat Xati shakllantiriladi.\n3. Shu raqam orqali siz bilan bog'lanishimiz mumkin.</code>",reply_markup=phone_uz)
    elif bot_language=='ru':
        await message.answer("<blockquote>✅ Принимаются тестовые предмет</blockquote>\n\n<i>Введите номер телефона.</i>\n+998 90 123 45 67\n<b>Набрав номер телефона</b>\n<code>1. Вы подтвердили, что логическая структура теста не содержит ошибок.\n2. Будет создано автоматическое гарантийное письмо.\n3. Мы можем связаться с вами по этому номеру.</code>",reply_markup=phone_ru)
    elif bot_language=='en':
        await message.answer("<blockquote>✅ Test subject accepted</blockquote>\n\n<i>Enter the phone number.</i>\n+998 90 123 45 67\n<b>By typing the phone number</b>\n<code>1. You have confirmed that the logical structure of the test is error-free.\n2. An Automatic Guarantee Letter will be generated.\n3. We can contact you through this number.</code>",reply_markup=phone_en)

    # Change state to groups
    await state.set_state(SendTest.phone_letter)

# Define a function to handle incoming subject
@router.message(SendTest.phone_letter, F.content_type.in_({'text', 'contact'}) )
async def handle_phone(message: types.Message, state: FSMContext):

    data = await state.get_data()
    bot_language = data.get('bot_lang')
    print("message.content_type0",message.content_type)
    if message.content_type=="contact":
        print("kirdim sho'ra")
        phone_num= message.contact.phone_number
    else:
        phone_num = message.text.strip()

    is_valid_phone = await valid_phone(phone_num)

    if is_valid_phone:
        # Update the state machine's data with the chosen data
        await state.update_data(
            {
                "phone": phone_num
            }
        )
        hemis_id = int(data.get('hemis_id'))
        
        try:
            db.update_user_phone(hemis_id=hemis_id,phone_num=phone_num)
        except sqlite3.IntegrityError as err:
            logging.info(f"Error: {err}")
        
        # chat_id = message.chat.id
        # # Delete the message
        # await delete_all_messages(chat_id)

        if bot_language=='uz':
            await message.answer("<blockquote>✅ Telefon raqam qabul qilindi</blockquote>\n\n<i>Kafedrani yozing</i>")
        elif bot_language=='ru':
            await message.answer("<blockquote>Номер телефона получен</blockquote>\n\n<i>Введите отдел</i>")
        elif bot_language=='en':
            await message.answer("<blockquote>Phone number received</blockquote>\n\n<i>Enter the department</i>")
        
        # Change state to groups
        await state.set_state(SendTest.test_department)

    else:
        if bot_language=='uz':
            await message.answer("⚠️ Telefon raqami xato! + ishorasiga e'tibor bering")
        elif bot_language=='ru':
            await message.answer("⚠️ Номер телефона указан неверно! Обратите внимание на знак +")
        elif bot_language=='en':
            await message.answer("⚠️ The phone number is wrong! Note the + sign")


# Define a function to handle incoming department
@router.message(SendTest.test_department)
async def handle_department(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')
    test_department = message.text.strip()
    # Update the state machine's data with the chosen data
    await state.update_data(
        {
            "test_department": test_department
        }
    )

    # chat_id = message.chat.id
    # # Delete the message
    # await delete_all_messages(chat_id)
    
    if bot_language=='uz':
        await message.answer("<blockquote>✅ Kafedra qabul qilindi</blockquote>\n\n<i>Testni qabul qilsak bo'ladimi?</i>",reply_markup=are_you_sure_markup)
    elif bot_language=='ru':
        await message.answer("<blockquote> ✅ Кафедра принята</blockquote>\n\n<i>Можем ли мы принять тест?</i>",reply_markup=are_you_sure_markup)
    elif bot_language=='en':
        await message.answer("<blockquote> ✅ Department accepted</blockquote>\n\n<i>Can we accept the test?</i>",reply_markup=are_you_sure_markup)

    # Change state to groups
    await state.set_state(SendTest.ready)