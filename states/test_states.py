from aiogram.fsm.state import StatesGroup, State

class SendTest(StatesGroup):
    test_file = State()
    groups = State()
    subject = State()
    phone_letter = State()
    test_department = State()
    ready = State()
