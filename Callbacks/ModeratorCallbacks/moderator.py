from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from Data.types.core import Core
from keyboards import moderator_keyboards as mdrt_kb
from States.State import ClientStateGroup

ModeratorRouter = Router()

@ModeratorRouter.callback_query(F.data == 'moder_create_client')
async def CreateClient(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(text='Введите имя и фамилию клиента через пробел', reply_markup=mdrt_kb.get_menu())
    await state.set_state(ClientStateGroup.create_client)

@ModeratorRouter.message(StateFilter(ClientStateGroup.create_client))
async def CreateClientName(m: Message, state: FSMContext):
    try:
        user_name, user_surname = m.text.split(' ')
    except Exception:
        await m.answer(text='Пожалуйста, введите имя и фамилию через пробел', reply_markup=mdrt_kb.get_menu())
    else:
        await m.answer(text='Введите номер телефона клиента', reply_markup=mdrt_kb.get_menu())
        await state.update_data(user_name=user_name, user_surname=user_surname)
        await state.set_state(ClientStateGroup.input_number)

@ModeratorRouter.message(StateFilter(ClientStateGroup.input_number))
async def InputNumber(m: Message, state: FSMContext):
    try:
        user_number = int(m.text)
    except Exception:
        await m.answer(text='Номер должен включать только числовые значения', reply_markup=mdrt_kb.get_menu())
    else:
        data = await state.get_data()
        user_name = data.get('user_name')
        user_surname = data.get('user_surname')
        await m.answer(text=f'Имя: {user_name}\nФамилия: {user_surname}\nТелефон: {user_number}\n\nВсе верно?',
                       reply_markup=mdrt_kb.confirm_crating_client())
        await state.update_data(user_number=user_number)
        
@ModeratorRouter.callback_query(F.data == 'confirm_crating_client')
async def ConfirmCreatingClient(c: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_surname = data.get('user_surname')
    user_number = data.get('user_number')
    await Core.CreateClient(user_name, user_surname, user_number)
    await c.message.edit_text(text=f'Карточка клиента {user_name} была создана✅', reply_markup=mdrt_kb.get_menu())