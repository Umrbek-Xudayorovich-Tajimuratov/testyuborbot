import os
from aiogram import types, F
from data.config import ROOT_PATH
from states.check_test_file import CheckTestState
from states.test_states import SendTest
from aiogram.fsm.context import FSMContext
from utils.check_test_file import check_tests, check_utf

from loader import router, bot
from utils.delete_message import delete_message



# Define a function to handle incoming files
@router.message(F.content_type == 'document', CheckTestState.check_test_file)
async def handle_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')
   

    if message.document.mime_type=='text/plain':

        # Get the document ID from the user
        file_id = message.document.file_id
        # Get the document file path from the file id
        fi = await bot.get_file(file_id)
        file_path = ROOT_PATH + fi.file_path
       
        # Check the file is in utf-8 format or not
        is_utf_8 = await check_utf(given_file=message.document, file_path=file_path)

        # If file is utf-8 format check test rules
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
                    await message.reply("<b>✅ Faylingiz xatosiz!</b>")
                elif bot_language=="en":
                    await message.reply("<b>✅ Your file is error free!</b>")
                elif bot_language=="ru":
                    await message.reply("<b>✅ Ваш файл без ошибок!</b>")
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
@router.message(F.content_type.not_in({'document'}), CheckTestState.check_test_file)
async def err_doc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')

    if bot_language=='uz':
        await message.answer("⚠️ Iltimos menga .txt file jo'nating!\n Emoji, gif, stiker, foto va video fayl qabul qilinmaydi!")
    elif bot_language=='ru':
        await message.answer("⚠️ Пожалуйста, пришлите мне файл .txt!\n Смайлики, гифки, стикеры, фото и видео не принимаются!")
    elif bot_language=='en':
        await message.answer("⚠️ Please send me a .txt file!\n Emoji, gif, sticker, photo and video files are not accepted!")

