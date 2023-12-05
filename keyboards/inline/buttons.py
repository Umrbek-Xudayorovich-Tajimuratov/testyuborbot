from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard = [[
    InlineKeyboardButton(text="✅ Ha/Yes/Да", callback_data='yes'),
    InlineKeyboardButton(text="❌ Yo'q/No/Нет", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
