from aiogram.fsm.state import StatesGroup, State

class SendTest(StatesGroup):
    test_file = State()
    groups = State()
    phone_letter = State()