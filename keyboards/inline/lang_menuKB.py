from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


langKB = [[
    InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='uz'),
    InlineKeyboardButton(text="🇷🇺 Русский ", callback_data='ru'),
    InlineKeyboardButton(text="🇬🇧 English ", callback_data='en'),
]]
lang_menu = InlineKeyboardMarkup(inline_keyboard=langKB)



