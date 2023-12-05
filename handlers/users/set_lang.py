from aiogram import types,F
from aiogram.fsm.context import FSMContext
from states.languages import Language
from states.user_login import UserData
from loader import router
from utils.delete_message import delete_message


# @router.callback_query(text="uz")
# @router.callback_query("uz")
# @router.callback_query((F.data =='uz') | (F.data =='ru') | (F.data =='en'))
@router.callback_query(Language.language)
async def bot_language(call: types.CallbackQuery, state: FSMContext):
    bot_language = call.data
    
    # Update the state machine's data with the chosen language
    await state.update_data(
        {
            "bot_lang": bot_language,
        })
    
    # chat_id = call.chat_instance
    # message_id = call.id
    # await delete_message(chat_id=chat_id,message_id=message_id)
   

    # Send the user notification message
    if   bot_language=='uz':
        await call.message.answer(f"<blockquote><b>Menu:</b> </blockquote>\n\nIltimos <code>HEMIS_ID</code> ni kiriting")
        # await call.message.answer(f"Iltimos <code>HEMIS_ID</code> ni kiriting")
    elif bot_language=='en':
        await call.message.answer(f"<blockquote><b>Language:</b> English</blockquote>\n\nPlease enter <code>HEMIS_ID</code>")
        # await call.message.answer(f"Please enter <code>HEMIS_ID</code>")
    elif bot_language=='ru':
        await call.message.answer(f"<blockquote><b>Язык:</b> Русский</blockquote>\n\nПожалуйста, введите <code>HEMIS_ID</code>")
        # await call.message.answer(f"Пожалуйста, введите <code>HEMIS_ID</code>")
    # else:
    #     await call.message.answer(f"Iltimos qayta urining\nПожалуйста, попробуйте еще раз\nPlease try again")
    await call.answer(cache_time=30)

    # Change state to hemis_id
    await state.set_state(UserData.hemis_id)
    # current_state = await state.get_state()
    # print(f"Current state: {current_state}")
    


    

    

   
