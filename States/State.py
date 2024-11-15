from aiogram.fsm.state import State, StatesGroup

class ClientStateGroup(StatesGroup):
    pagination = State()

    add_moder = State()
    confirm_adding = State()

    change_number = State()
    confirm_change_number = State()

    increase_bonuses_moder = State()
    increase_bonuses_admn = State()
    confirm_increasing = State()

    decrease_bonuses_moder = State()
    decrease_bonuses_admn = State()
    confirm_decreasing = State()

    create_client = State()
    input_number = State()

    find_client_number = State()
    find_client_id = State()
    moderator_panel = State()