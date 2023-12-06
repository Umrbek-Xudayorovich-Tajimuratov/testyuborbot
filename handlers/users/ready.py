from aiogram import types,F
from aiogram.fsm.context import FSMContext
from data.config import CHANNEL_ID
from states.home import HomeState
from states.test_states import SendTest
from keyboards.reply.home import home_en,home_ru,home_uz
from loader import bot
from loader import router
import json



@router.callback_query(SendTest.ready)
async def test_ready(call: types.CallbackQuery, state: FSMContext):
    data =  await state.get_data()
    bot_language = data.get('bot_lang')

    if call.data=="yes":
        hemis_id = data.get('hemis_id')
        password = data.get('password')
        teacher_name = data.get("name")
        department = json.loads(data.get('department'))
        staff_position = json.loads(data.get('staff_position'))
        subject = data.get("subject")
        groups = data.get("groups")
        file_id = data.get("file_id")
        phone = data.get("phone")
        test_department = data.get('test_department')

        dep_staf = ''
        for index in range(len(department)):
            if bot_language == 'uz':
                dep_staf += f"\n<i><b>⛺️ KAFEDRA{index+1}:</b></i> <code>{department[index]}</code>\n<i><b>🧰 LAVOZIM{index+1}:</b></i> <code>{staff_position[index]}</code>"
            elif bot_language == 'ru':
                dep_staf += f"\n<i><b>⛺️ ОТДЕЛ{index+1}:</b></i> <code>{department[index]}</code>\n<i><b>🧰 ДОЛЖНОСТЬ{index+1}:</b></i> <code>{staff_position[index]}</code>"
            elif bot_language == 'en':
                dep_staf += f"\n<i><b>⛺️ DEPARTMENT{index+1}:</b></i> <code>{department[index]}</code>\n<i><b>🧰 POSITION{index+1}:</b></i> <code>{staff_position[index]}</code>"

        
        admin_cap = f"\
            <i><b>🆔 HEMIS_ID:</b></i> <code>{hemis_id}</code>\
            \n<i><b>🔐 Parol:</b></i> <code>{password}</code>\
            \n<i><b>👨‍⚖️ Username:</b></i> <code>{call.from_user.username}</code>\
            \n<i><b>👨‍⚖️ Link:</b></i> <a href='tg://user?id={call.from_user.id}'>{call.from_user.full_name}</a>\
            {dep_staf}\
            \n\n<i><b>👨‍🏫 Ism:</b></i> <code>{teacher_name}</code>\
            \n<i><b>📚 Fan:</b></i> <code>{subject}</code>\
            \n<i><b>👥 Guruhlar:</b></i> <code>{groups}</code>\
            \n<i><b>🏢 Kafedra:</b></i> <code>{test_department}</code>\
            \n<i><b>📲 Telefon:</b></i> <code>{phone}</code>\
        "
        user_cap_uz=f"\
            <i><b>👨‍🏫 Ism:</b></i> <code>{teacher_name}</code>\
            \n<i><b>📚 Fan:</b></i> <code>{subject}</code>\
            \n<i><b>👥 Guruhlar:</b></i> <code>{groups}</code>\
            \n<i><b>🏢 Kafedra:</b></i> <code>{test_department}</code>\
            \n<i><b>📲 Telefon:</b></i> <code>{phone}</code>\
            \n\nYana boshqa test yuklashingiz mumkin  \
        "
        user_cap_ru=f"\
            <i><b>👨‍🏫 Имя:</b></i> <code>{teacher_name}</code>\
            \n<i><b>📚 Наука:</b></i> <code>{subject}</code>\
            \n<i><b>👥 Группы:</b></i> <code>{groups}</code>\
            \n<i><b>🏢 Отдел:</b></i> <code>{test_department}</code>\
            \n<i><b>📲 Телефон:</b></i> <code>{phone}</code>\
            \n\nВы можете загрузить другой тест  \
        "
        user_cap_en=f"\
            <i><b>👨‍🏫 Name:</b></i> <code>{teacher_name}</code>\
            \n<i><b>📚 Subject:</b></i> <code>{subject}</code>\
            \n<i><b>👥 Groups:</b></i> <code>{groups}</code>\
            \n<i><b>🏢 Department:</b></i> <code>{test_department}</code>\
            \n<i><b>📲 Phone:</b></i> <code>{phone}</code>\
            \n\nYou can load another test  \
        "
    
        # Send the test  to the Admin and user
        chat_id = call.from_user.id
        if bot_language == 'uz':
            await bot.send_document(document=file_id, caption=user_cap_uz, chat_id=chat_id,reply_markup=home_uz)
        elif bot_language == 'ru':
            await bot.send_document(document=file_id, caption=user_cap_ru, chat_id=chat_id,reply_markup=home_ru)
        elif bot_language == 'en':
            await bot.send_document(document=file_id, caption=user_cap_en, chat_id=chat_id,reply_markup=home_en)

        await bot.send_document(document=file_id, caption=admin_cap, chat_id=CHANNEL_ID[0])

    else:
        if bot_language == 'uz':
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"🚫 <b>TEST YUKLANMADI!</b>\n\nTest yuklashni qaytadan boshlashingiz mumkin!",reply_markup=home_uz)
        elif bot_language == 'ru':
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"🚫 <b>ТЕСТ НЕ ЗАГРУЗИЛСЯ!</b>\n\nВы можете перезапустить тестовую загрузку!",reply_markup=home_ru)
        elif bot_language == 'en':
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"🚫 <b>TEST FAILED TO LOAD!</b>\n\nYou can restart test loading!",reply_markup=home_en)

    # # Reset the FSM to the start state
    # await state.clear()

    # Change state to groups
    await state.set_state(HomeState.choose_menu)