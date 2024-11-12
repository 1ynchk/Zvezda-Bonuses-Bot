from aiogram.fsm.state import State, StatesGroup

class ClientStateGroup(StatesGroup):
    pagination = State()

    add_moder = State()
    confirm_adding = State()