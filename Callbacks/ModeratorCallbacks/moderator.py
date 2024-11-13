from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from Data.types.core import Core
from keyboards import moderator_keyboards as mdrt_kb
from keyboards import admin_keyboards as admn_kb
from States.State import ClientStateGroup

import os 
import dotenv

dotenv.load_dotenv()

ModeratorRouter = Router()

@ModeratorRouter.callback_query(F.data == 'moder_create_client')
async def CreateClient(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(text='Введите имя и фамилию клиента через пробел', reply_markup=mdrt_kb.get_moderator_menu())
    await state.set_state(ClientStateGroup.create_client)

@ModeratorRouter.message(StateFilter(ClientStateGroup.create_client))
async def CreateClientName(m: Message, state: FSMContext):
    try:
        user_name, user_surname = m.text.split(' ')
    except Exception:
        await m.answer(text='Пожалуйста, введите имя и фамилию через пробел', reply_markup=mdrt_kb.get_moderator_menu())
    else:
        await m.answer(text='Введите номер телефона клиента', reply_markup=mdrt_kb.get_moderator_menu())
        await state.update_data(user_name=user_name, user_surname=user_surname)
        await state.set_state(ClientStateGroup.input_number)

@ModeratorRouter.message(StateFilter(ClientStateGroup.input_number))
async def InputNumber(m: Message, state: FSMContext):
    try:
        user_number = int(m.text)
    except Exception:
        await m.answer(text='Номер должен включать только числовые значения', reply_markup=mdrt_kb.get_moderator_menu())
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
    await c.bot.send_message(
        chat_id=os.getenv('ADMIN'), 
        text=f'Модератор {c.from_user.username} создал карточку клиенту {user_name} 👨‍🔧',
        reply_markup=admn_kb.get_menu())
    await c.message.edit_text(text=f'Карточка клиента {user_name} была создана✅', reply_markup=mdrt_kb.get_moderator_menu())

@ModeratorRouter.callback_query(F.data == 'moder_find_client')
async def FindCLietn(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(text='Введите номер клиента', reply_markup=mdrt_kb.get_moderator_menu())
    await state.set_state(ClientStateGroup.find_client)


@ModeratorRouter.message(StateFilter(ClientStateGroup.find_client))
async def StateFindClient(m: Message, state: FSMContext):
    try:
        number = int(m.text)
    except Exception:
        await m.answer(text='Номер должен включать только числовые значения', reply_markup=mdrt_kb.get_moderator_menu())
    else:
        user = await Core.FindClient(str(number))

        if user == False:
            await m.answer(text='Пользователя с таким номером нет, для повторного поиска напишите номер еще раз', reply_markup=mdrt_kb.get_moderator_menu())
        else:
            user_name = user[0]
            user_surname = user[1]
            user_number = user[2]
            user_bonuses = user[3]
            await m.answer(
                text=f'<b>Имя:</b> {user_name}\n<b>Фамилия:</b> {user_surname}\n<b>Номер тел.:</b> {user_number}\n<b>Бонусы:</b> {user_bonuses}',
                parse_mode='HTML',
                reply_markup=mdrt_kb.get_menu_client())
            await state.set_state(ClientStateGroup.moderator_panel)
            await state.update_data(user_name=user_name, user_number=user_number)

@ModeratorRouter.callback_query(F.data == 'increase_bonuses_moder')
async def IncreaseBonuses(c: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    
    await c.message.edit_text(text=f'Укажите кол-во начисляемых баллов для {user_name}', 
                              reply_markup=mdrt_kb.get_moderator_menu())
    
    await state.set_state(ClientStateGroup.increase_bonuses)

@ModeratorRouter.message(StateFilter(ClientStateGroup.increase_bonuses))
async def IncreaseBonusesState(m: Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')

    try:
        value = int(m.text)
    except Exception:
        await m.answer(text='Введите целое числовое значение превышающее 0', reply_markup=mdrt_kb.get_moderator_menu())
    else:
        if value <= 0:
            await m.answer(text='Значение должно быть больше 0', reply_markup=mdrt_kb.get_moderator_menu())
        else:
            await m.answer(text=f'Вы подтверждаете начисление {value} баллов клиенту {user_name}?', reply_markup=mdrt_kb.confirm_increasing_bonuses())
            await state.set_state(ClientStateGroup.confirm_increasing)
            await state.update_data(value=value)

@ModeratorRouter.callback_query(F.data == 'confirm_increasing_bonuses_moder')
async def ConfirmIncreasingBonuses(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_number = data.get('user_number')
    value = data.get('value')

    await Core.IncreaseBonuses(user_number, value)
    await c.bot.send_message(
        chat_id=os.getenv('ADMIN'), 
        text=f'Модератор {c.from_user.username} начислил {value} бонусов клиенту {user_name} 👨‍🔧',
        reply_markup=admn_kb.get_menu())
    await c.message.edit_text(text=f'Баллы были начислены {user_name}✅', reply_markup=mdrt_kb.get_moderator_menu())

@ModeratorRouter.callback_query(F.data == 'decrease_bonuses_moder')
async def DecreaseBonuses(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    await c.message.edit_text(text=f'Вы подтверждаете снятие баллов у клиента {user_name}?', reply_markup=mdrt_kb.confirm_decreasing_bonuses())
    await state.set_state(ClientStateGroup.confirm_decreasing)

@ModeratorRouter.callback_query(F.data == 'confirm_decreasing_bonuses_moder')
async def ConfirmDecreasingBonuses(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_number = data.get('user_number')

    await Core.DecreaseBonuses(user_number)
    await c.bot.send_message(
        chat_id=os.getenv('ADMIN'), 
        text=f'Модератор {c.from_user.username} снял бонусы клиенту {user_name} 👨‍🔧',
        reply_markup=admn_kb.get_menu())
    await c.message.edit_text(text=f'Баллы сняты у {user_name}✅', reply_markup=mdrt_kb.get_moderator_menu())