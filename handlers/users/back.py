from aiogram import types,F
from aiogram.fsm.context import FSMContext
from states.check_test_file import CheckTestState
from states.languages import Language
from keyboards.reply.home import home_uz, home_ru, home_en
from keyboards.reply.back import back_en, back_uz, back_ru
from keyboards.reply.phone_sendingKB import phone_en, phone_ru,phone_uz
from states.home import HomeState
from loader import router,bot
from states.test_states import SendTest
from states.user_login import UserData
from utils.delete_message import delete_message

@router.message(F.text.in_ ({"🏘 Bosh menu","🏘 Main menu","🏘 Главное меню"}))
@router.message(F.text.in_ ({"🔙 Ortga","🔙 Back","🔙 Назад"}))
async def go_back(message: types.Message, state: FSMContext):
    data = await state.get_data()
    bot_language = data.get('bot_lang')

    is_main_btn = message.text in ["🏘 Bosh menu","🏘 Main menu","🏘 Главное меню"]

    current_state = await state.get_state()
    if current_state==CheckTestState.check_test_file or current_state==UserData.hemis_id or current_state==HomeState.info or ( (current_state==UserData.hemis_password or current_state==SendTest.test_file or current_state==SendTest.groups or SendTest.phone_letter or SendTest.test_department or SendTest.ready) and is_main_btn):
        if bot_language=="uz":
            await message.answer('<b>BOSH MENU</b>', reply_markup=home_uz)
        elif bot_language=="en":
            await message.answer('<b>MAIN MENU</b>', reply_markup=home_en)
        elif bot_language=="ru":
            await message.answer('<b>ГЛАВНОЕ МЕНЮ</b>', reply_markup=home_ru)

        # Change state to choose_menu
        await state.set_state(HomeState.choose_menu)
    
    elif current_state==UserData.hemis_password:
        if bot_language=="uz":
            await message.answer('<code>HEMIS_ID</code> ni kiriting', reply_markup=back_uz)
        elif bot_language=="en":
            await message.answer('Please enter <code>HEMIS_ID</code>', reply_markup=back_en)
        elif bot_language=="ru":
            await message.answer('Пожалуйста, введите <code>HEMIS_ID</code>', reply_markup=back_ru)

        # Change state to hemis_id
        await state.set_state(UserData.hemis_id)

    elif current_state==SendTest.test_file:
        if bot_language=='uz':
            await message.answer(f"🔐 Parolni kiriting\n",reply_markup=back_uz)
        elif bot_language=='ru':
            await message.answer(f"🔐 Введите пароль\n",reply_markup=back_ru)
        elif bot_language=='en':
            await message.answer(f"🔐 Enter the Password\n",reply_markup=back_en)

        # Change state to hemis_password
        await state.set_state(UserData.hemis_password)

    elif current_state==SendTest.groups:
        if bot_language=="uz":
            msg_one = "<i>Jo'natmoqchi bo'lgan test (.txt) faylini yuklang</i>"
            await message.answer(msg_one, reply_markup=back_uz)
        elif bot_language=="en":
            msg_one = "<i>Upload the test (.txt) file you want to send</i>"
            await message.answer(msg_one, reply_markup=back_en)
        elif bot_language=="ru":
            msg_one = "<i>Загрузите тестовый файл (.txt), который хотите отправить</i>"
            await message.answer(msg_one, reply_markup=back_ru)

        # Change state to test_file
        await state.set_state(SendTest.test_file)

    elif current_state==SendTest.subject:
        if bot_language=="uz":
            await message.reply("<i>Test topshiradigan guruhlarni yozing</i>",reply_markup=back_uz)
        elif bot_language=="en":
            await message.reply("<i>Type the groups which the test will be taken</i>",reply_markup=back_en)
        elif bot_language=="ru":
            await message.reply("<i>Укажите группы, для которых будет проводиться тест</i>",reply_markup=back_ru)
        
        # Change state to groups
        await state.set_state(SendTest.groups)

    elif current_state == SendTest.phone_letter:
        if bot_language=='uz':
            await message.answer("<i>📖 Fan nomini o'zbekcha yozing</i>")
        elif bot_language=='ru':
            await message.answer("<i>📖 Напишите название предмета на узбекском языке</i>")
        elif bot_language=='en':
            await message.answer("<i>📖 Write the name of the subject in Uzbek</i>")

        # Change state to subject
        await state.set_state(SendTest.subject)
    
    elif current_state==SendTest.test_department:
        if bot_language=='uz':
            await message.answer("<i>Telefon raqamini kiriting.</i>\n+998 90 123 45 67",reply_markup=phone_uz)
        elif bot_language=='ru':
            await message.answer("<i>Введите номер телефона.</i>\n+998 90 123 45 67",reply_markup=phone_ru)
        elif bot_language=='en':
            await message.answer("<i>Enter the phone number.</i>\n+998 90 123 45 67",reply_markup=phone_en)

        # Change state to phone_letter
        await state.set_state(SendTest.phone_letter)

    elif current_state==SendTest.ready:
        if bot_language=='uz':
            await message.answer("<i>Kafedrani yozing</i>")
        elif bot_language=='ru':
            await message.answer("<i>Введите отдел</i>")
        elif bot_language=='en':
            await message.answer("<i>Enter the department</i>")
        
        # Change state to test_department
        await state.set_state(SendTest.test_department)