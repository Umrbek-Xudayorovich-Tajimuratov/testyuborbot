import aiogram
import logging
from loader import bot
# from aiogram.dispatcher.fsm import FSMDispatcher

# # todo: delete all chat messages
# dispatcher = FSMDispatcher(bot)
# async def get_chat_history(chat_id, offset, limit):
#     messages = await dispatcher.get_chat_history(chat_id=chat_id, offset=offset, limit=limit)
#     return messages


# async def delete_all_messages(chat_id):
#     offset = 0
#     limit = 100

#     while True:
#         messages = await get_chat_history(chat_id=chat_id, offset=offset, limit=limit)

#         if not messages:
#             break

#         for message in messages:
#             await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

#         offset += limit
# # todo: delete all chat messages--------------


async def delete_message(message_id, chat_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.exception(e)



# async def delete_all_messages(chat_id,chat_type):
#     offset = 0
#     limit = 100

#     while True:
#         chat = aiogram.types.Chat(id=chat_id, type='private')
#         messages = await chat.get_history(offset=offset, limit=limit)
#         # messages = await bot.get_chat_history(chat_id=chat_id, offset=offset, limit=limit)

#         if not messages:
#             break

#         for message in messages:
#             await bot.delete_message(chat_id=chat_id, message_id=message.message_id)

#         offset += limit