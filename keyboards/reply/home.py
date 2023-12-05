from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

home_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✔️ Testni tekshirish"),
            KeyboardButton(text="🗃️ Testni yuklash"),
        ],
        [
            KeyboardButton(text="⚖️ Test yuborish qoidalari"),
        ],
        [
            KeyboardButton(text="🌏 Tilni o'zgartirish"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Kerakli bo'limni tanlang"
)

home_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✔️ Проверьте тест"),
            KeyboardButton(text="🗃️ Загрузить тест"),
        ],
        [
            KeyboardButton(text="⚖️ Правила отправки тестов"),
        ],
        [
            KeyboardButton(text="🌏 Изменить язык"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите нужный раздел"
)

home_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✔️ Check the test"),
            KeyboardButton(text="🗃️ Upload the test"),
        ],
        [
            KeyboardButton(text="⚖️ Test submission rules"),
        ],
        [
            KeyboardButton(text="🌏 Changing language"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Select the desired section"
)