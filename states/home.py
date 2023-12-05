from aiogram.fsm.state import StatesGroup, State

class HomeState(StatesGroup):
    home_state = State()
    choose_menu = State()
    info = State()