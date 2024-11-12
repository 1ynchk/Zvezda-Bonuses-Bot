from aiogram.fsm.state import State, StatesGroup

class ClientStateGroup(StatesGroup):
    pagination = State()

    add_moder = State()
    confirm_adding = State()

    increase_bonuses = State()
    confirm_increasing = State()
    confirm_decreasing = State()