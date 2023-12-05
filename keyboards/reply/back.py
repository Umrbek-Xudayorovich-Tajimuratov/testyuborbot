from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_uz = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🏘 Bosh menu"),
        KeyboardButton(text="🔙 Ortga"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_en = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🏘 Main menu"),
        KeyboardButton(text="🔙 Back"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_ru = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🏘 Главное меню"),
        KeyboardButton(text="🔙 Назад"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_alone_uz = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🔙 Ortga"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_alone_en = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🔙 Back"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)

back_alone_ru = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🔙 Назад"),
    ],],
    resize_keyboard=True,
    one_time_keyboard=True
)