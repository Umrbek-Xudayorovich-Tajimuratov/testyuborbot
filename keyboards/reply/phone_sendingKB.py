from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Telefon raqamimni yuborish", request_contact=True),
        ],
        [
            KeyboardButton(text="🏘 Bosh menu"),
            KeyboardButton(text="🔙 Ortga"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
phone_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Отправьте мой номер телефона", request_contact=True),
        ],
        [
            KeyboardButton(text="🏘 Главное меню"),
            KeyboardButton(text="🔙 Назад"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
phone_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Send my phone number", request_contact=True),
        ],
        [
            KeyboardButton(text="🏘 Main menu"),
            KeyboardButton(text="🔙 Back"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
