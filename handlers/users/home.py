from aiogram import types,F
from aiogram.fsm.context import FSMContext
from states.check_test_file import CheckTestState
from states.languages import Language
from keyboards.reply.home import home_uz, home_ru, home_en
from keyboards.reply.back import back_en, back_uz, back_ru, back_alone_en,back_alone_uz,back_alone_ru
from states.home import HomeState
from loader import router,bot
from states.user_login import UserData
from utils.delete_message import delete_message

@router.callback_query(HomeState.home_state)
async def home_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=30)

    bot_language = call.data
    # Update the state machine's data with the chosen language
    await state.update_data(
        {
            "bot_lang": bot_language,
        }
    )
    data = await state.get_data()

    # Delete previous message
    del_msg = data.get('del_msg')
    await delete_message(chat_id=call.from_user.id,message_id=del_msg.message_id)
   

    # Send the user notification message
    if   bot_language=='uz':
        await call.message.answer(f"<blockquote><b>TIL:</b> O'zbek</blockquote>\n\n<b>Menudan tanlang</b>", reply_markup=home_uz)
        # await call.message.answer(f"Iltimos <code>HEMIS_ID</code> ni kiriting")
    elif bot_language=='en':
        await call.message.answer(f"<blockquote><b>Language:</b> English</blockquote>\n\n<b>Select from menu</b>", reply_markup=home_en)
        # await call.message.answer(f"Please enter <code>HEMIS_ID</code>")
    elif bot_language=='ru':
        await call.message.answer(f"<blockquote><b>Язык:</b> Русский</blockquote>\n\n<b>Выберите из меню</b>", reply_markup=home_ru)
        # await call.message.answer(f"Пожалуйста, введите <code>HEMIS_ID</code>")
    # else:
    #     await call.message.answer(f"Iltimos qayta urining\nПожалуйста, попробуйте еще раз\nPlease try again")

    # Change state to choose_menu
    await state.set_state(HomeState.choose_menu)
    


@router.message(F.text.in_ ({"🗃️ Testni yuklash","🗃️ Загрузить тест","🗃️ Upload the test"}), HomeState.choose_menu)
async def upload_test(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')

    if   bot_language=='uz':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\nIltimos <code>HEMIS_ID</code> ni kiriting", reply_markup=back_alone_uz)
    elif bot_language=='en':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\nPlease enter <code>HEMIS_ID</code>", reply_markup=back_alone_en)
    elif bot_language=='ru':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\nПожалуйста, введите <code>HEMIS_ID</code>", reply_markup=back_alone_ru)
    # await message.answer(cache_time=30)
    
    # Change state to hemis_id
    await state.set_state(UserData.hemis_id)



@router.message(F.text.in_ ({"✔️ Testni tekshirish","✔️ Проверьте тест","✔️ Check the test"}), HomeState.choose_menu)
async def checking_tes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')


    if bot_language=='uz':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\n📥 <i>Test (.txt) faylini yuklang</i>", reply_markup=back_alone_uz)
    elif bot_language=='en':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\n📥 <i>Upload the test (.txt) file</i>", reply_markup=back_alone_en)
    elif bot_language=='ru':
        await message.answer(f"<blockquote><b>MENU:</b> {message.text}</blockquote>\n\n📥 <i>Загрузите тестовый файл (.txt)</i>", reply_markup=back_alone_ru)
    # await message.answer(cache_time=30)

    # Change state to check_test_file
    await state.set_state(CheckTestState.check_test_file)


@router.message(F.text.in_ ({"⚖️ Test yuborish qoidalari","⚖️ Правила отправки тестов","⚖️ Test submission rules"}), HomeState.choose_menu)
async def rules_reminder(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')


    if bot_language=='uz':
        btn = back_alone_uz
        msg = f"<blockquote>{message.text}</blockquote>\n\
____\n\
1. <code>Savollar <b>.txt</b> faylida va <b>utf-8</b> formatida bo'lishi kerak</code>\n\
____\n\
2. <code>Savollar kamida 60 ta bo'lishi kerak</code>\n\
____\n\
3. <code>Savolning boshi <b>A.</b> kabi ko'rinishda boshlanishi mumkin emas.\nMasalan: I. Karimov kim?</code>\n\
____\n\
4. <code>Savol va Javoblar 2 yoki undan ko'p qator bo'lmasligi kerak</code>\n\
____\n\
5. <code>Javoblar katta harflarda va A. B. C. D. ko'rinishida 4 ta variantdan iborat bo'lishi kerak </code>\n\
____\n\
6. <code>Javoblar A. B. C. D. va ANSWER: A lotin harflarida bo'lishi shart.</code>\n\
____\n\
7. <code>Na'munaga e'tibor bering.</code>\
"
        
    elif bot_language=='en':
        btn = back_alone_en
        msg = f"<blockquote>{message.text}</blockquote>\n\
____\n\
1. <code>Questions must be in <b>.txt</b> file and <b>utf-8</b> format</code>\n\
____\n\
2. <code>There should be at least 60 questions</code>\n\
____\n\
3. <code>The beginning of the question cannot start in the form of <b>A.</b>.\nFor example: Who is I. Karimov?</code>\n\
____\n\
4. <code>Questions and Answers should not be 2 or more lines</code>\n\
____\n\
5. <code>Answers must be in capital letters and have 4 options in the form A. B. C. D. </code>\n\
____\n\
6. <code>Answers must be in Latin letters A. B. C. D. and ANSWER: A</code>\n\
____\n\
7. <code>Pay attention to the pattern.</code>\
"
    elif bot_language=='ru':
        btn = back_alone_ru
        msg = f"<blockquote>{message.text}</blockquote>\n\
____\n\
1. <code>Вопросы должны быть в файле <b>.txt</b> и формате <b>utf-8</b></code>\n\
____\n\
2. <code>Вопросов должно быть не менее 60</code>\n\
____\n\
3. <code>Начало вопроса не может начинаться в форме <b>A.</b>\nНапример: И.Каримов кто такой ?</code>\n\
____\n\
4. <code>Вопросы и ответы не должны состоять из 2 и более строк</code>\n\
____\n\
5. <code>Ответы должны быть написаны заглавными буквами и иметь 4 варианта в виде A.B.C.D.</code>\n\
____\n\
6. <code>Ответы должны быть латинскими буквами A. B. C. D. и ANSWER: A</code>\n\
____\n\
7. <code>Обратите внимание на узор.</code>\
    "
    # await message.answer(cache_time=30)

    # Send correct file to user
    file_path = "documents/namuna.txt"
    input_file = types.FSInputFile(file_path)
    await bot.send_document(document=input_file, caption=msg, chat_id=message.chat.id, reply_markup=btn)

    # Change state to info
    await state.set_state(HomeState.info)

