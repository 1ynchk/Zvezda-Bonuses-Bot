from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from Data.types.core import Core
from keyboards import admin_keyboards as admn_kb
from Common import pagination as pag
from States.State import ClientStateGroup

AdminCallbackRouter = Router()

@AdminCallbackRouter.callback_query(F.data == 'admin_moderators')
async def ModeratorsList(c: CallbackQuery, state: FSMContext):
    res = await Core.GetAllModerators() 

    if res == None or len(res) == 0:
        await c.message.edit_text(text="Модераторов еще нет",reply_markup=admn_kb.get_menu())
    else:
        dictionary, keyboard = await pag.make_caption_users(res, 'Moderators')
        await c.message.edit_text(text=dictionary["1"][0]["str_stuff"], reply_markup=keyboard, parse_mode="MarkDownV2")

        await state.set_state(ClientStateGroup.pagination)
        await state.update_data(dictionary=dictionary, current_page=1, statement="Moderators")

@AdminCallbackRouter.callback_query(F.data.startswith('moderator_'))
async def DeleteModerator(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    values_index, sheet  = [str(x) for x in c.data[10:].split("_")]

    if sheet == '1':
        user_name = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][0]
        user_id = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][1]
    else:

        user_name = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][0]
        user_id = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][1]
    await c.message.edit_text(text=f"Вы точно хотите удалить модератора {user_name}?", 
                                reply_markup=admn_kb.confirm_blocking_moderator())
    await state.update_data(blocked_user=(user_id, user_name))

@AdminCallbackRouter.callback_query(F.data == 'confirm_blocking_moderator')
async def ConfirmBLockingModerator(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id, user_name = data.get("blocked_user")
    await Core.DeleteModerator(user_id, user_name)
    await c.message.edit_text(text=f'Модератор {user_name} был удален ✅', reply_markup=admn_kb.get_menu())

@AdminCallbackRouter.callback_query(F.data == 'admin_add_moderator')
async def AddModerator(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text(text='Введите Телеграм username модератора', reply_markup=admn_kb.get_menu())
    await state.set_state(ClientStateGroup.add_moder)

@AdminCallbackRouter.message(StateFilter(ClientStateGroup.add_moder))
async def AddModeratorState(m: Message, state: FSMContext):
    try:
        int(m.text)
    except Exception:
        await state.set_state(ClientStateGroup.confirm_adding)
        if m.text[0] == '@':
            moderator = m.text[1:]
        else:
            moderator = m.text
        await m.answer(text=f'Создать роль модератора для {moderator}?', reply_markup=admn_kb.confirm_creating_moderator())
        await state.update_data(moderator=moderator)
    else:
        await m.answer(text='Не валидный username', reply_markup=admn_kb.get_menu())
    
@AdminCallbackRouter.callback_query(F.data == 'confirm_creating_moderator')
async def ConfirmCreatingModerator(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    moderator = data.get('moderator')
    await Core.CreateModerator(moderator)
    await c.message.edit_text(text=f'Роль модератора была успешно создана для {moderator}✅', reply_markup=admn_kb.get_menu())

@AdminCallbackRouter.callback_query(F.data == 'admin_clients')
async def ModeratorsList(c: CallbackQuery, state: FSMContext):
    res = await Core.GetAllClients() 

    if res == None or len(res) == 0:
        await c.message.edit_text(text="Клиентов еще нет",reply_markup=admn_kb.get_menu())
    else:
        dictionary, keyboard = await pag.make_caption_users(res, 'Clients')
        await c.message.edit_text(text=dictionary["1"][0]["str_stuff"], reply_markup=keyboard, parse_mode="MarkDownV2")

        await state.set_state(ClientStateGroup.pagination)
        await state.update_data(dictionary=dictionary, current_page=1, statement="Clients")

@AdminCallbackRouter.callback_query(F.data.startswith('client_'))
async def ClientInfo(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    values_index, sheet  = [str(x) for x in c.data[7:].split("_")]

    if sheet == '1':
        user_name = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][0]
        user_surname = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][1]
        user_number = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][2]
        user_bonuses = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][3]
        user_id = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index)-1][4]
    else:
        user_name = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][0]
        user_surname = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][1]
        user_number = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][2]
        user_bonuses = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][3]
        user_id = data.get("dictionary")[sheet][0]["values_stuff"][int(values_index) + (int(sheet) - 1) * 10 - 1][4]
    user_bonuses = 0 if user_bonuses == None else user_bonuses
    text = f"<b>ID:</b> {user_id}\n<b>Имя:</b> {user_name}\n<b>Фамилия:</b> {user_surname}\n<b>Номер тел.:</b> {user_number}\n<b>Бонусы:</b> {user_bonuses}"
    await c.message.edit_text(text=text, reply_markup=admn_kb.get_menu_client(), parse_mode='HTML')
    await state.update_data(user_name=user_name, user_id=user_id, user_surname=user_surname, user_number=user_number)

@AdminCallbackRouter.callback_query(F.data == 'change_number')
async def ChangeNumber(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    await c.message.edit_text(text=f'Введите новый номер клиента {user_name}', reply_markup=admn_kb.get_menu())
    await state.set_state(ClientStateGroup.change_number)

@AdminCallbackRouter.message(StateFilter(ClientStateGroup.change_number))
async def StateChangeNumber(m: Message, state: FSMContext):
    try:
        user_number = int(m.text)
    except Exception:
        await m.answer(text='Номер должен включать только числовые значения', reply_markup=admn_kb.get_menu())
    else:
        data = await state.get_data()
        user_name = data.get('user_name')
        await m.answer(text=f'Изменить номер клиента {user_name}?', reply_markup=admn_kb.confirm_changing_number())
        await state.set_state(ClientStateGroup.confirm_change_number)
        await state.update_data(user_number = user_number)

@AdminCallbackRouter.callback_query(F.data == 'confirm_changing_number')
async def ConfirmChangingNumber(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    user_number = data.get('user_number')
    await Core.ChangeNumber(user_id, str(user_number))
    await c.message.edit_text(text=f'Номер пользователя {user_name} был изменен✅', reply_markup=admn_kb.get_menu())
    await state.clear()
    
@AdminCallbackRouter.callback_query(F.data == 'admin_delete_client')
async def DeleteClient(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')

    await c.message.edit_text(text=f'Вы точно хотите удалить клиента {user_name}?', reply_markup=admn_kb.confirm_blocking_client())

@AdminCallbackRouter.callback_query(F.data == 'confirm_blocking_client')
async def ConfirmDeletingClient(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    user_number = data.get('user_number')

    await Core.DeleteClient(user_id, user_number)
    await c.message.edit_text(text=f'Клиент {user_name} был успешно удален✅', reply_markup=admn_kb.get_menu())

@AdminCallbackRouter.callback_query(F.data == 'increase_bonuses')
async def IncreaseBonuses(c: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    
    await c.message.edit_text(text=f'Укажите кол-во начисляемых баллов для {user_name}', 
                              reply_markup=admn_kb.get_menu())
    
    await state.set_state(ClientStateGroup.increase_bonuses_admn)

@AdminCallbackRouter.message(StateFilter(ClientStateGroup.increase_bonuses_admn))
async def IncreaseBonusesState(m: Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')

    try:
        value = int(m.text)
    except Exception:
        await m.answer(text='Введите целое числовое значение превышающее 0', reply_markup=admn_kb.get_menu())
    else:
        if value <= 0:
            await m.answer(text='Значение должно быть больше 0', reply_markup=admn_kb.get_menu())
        else:
            await m.answer(text=f'Вы подтверждаете начисление {value} баллов клиенту {user_name}?', reply_markup=admn_kb.confirm_increasing_bonuses())
            await state.set_state(ClientStateGroup.confirm_increasing)
            await state.update_data(value=value)

@AdminCallbackRouter.callback_query(F.data == 'confirm_increasing_bonuses_admn')
async def ConfirmIncreasingBonuses(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_number = data.get('user_number')
    value = data.get('value')

    await Core.IncreaseBonuses(user_number, value)
    await c.message.edit_text(text=f'Баллы были начислены {user_name}✅', reply_markup=admn_kb.get_menu())

@AdminCallbackRouter.callback_query(F.data == 'decrease_bonuses_admn')
async def IncreaseBonuses(c: CallbackQuery, state:FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    
    await c.message.edit_text(text=f'Укажите кол-во снимаемых баллов у {user_name}', 
                              reply_markup=admn_kb.get_menu())
    
    await state.set_state(ClientStateGroup.decrease_bonuses_admn)

@AdminCallbackRouter.message(StateFilter(ClientStateGroup.decrease_bonuses_admn))
async def IncreaseBonusesState(m: Message, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')

    try:
        value = int(m.text)
    except Exception:
        await m.answer(text='Введите целое числовое значение превышающее 0', reply_markup=admn_kb.get_menu())
    else:
        if value <= 0:
            await m.answer(text='Значение должно быть больше 0', reply_markup=admn_kb.get_menu())
        else:
            await m.answer(text=f'Вы подтверждаете снятие {value} баллов у клиента {user_name}?', reply_markup=admn_kb.confirm_decreasing_bonuses())
            await state.set_state(ClientStateGroup.confirm_decreasing)
            await state.update_data(value=value)

@AdminCallbackRouter.callback_query(F.data == 'confirm_decreasing_bonuses_admn')
async def ConfirmDecreasingBonuses(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_name = data.get('user_name')
    user_number = data.get('user_number')
    value = data.get('value')

    await Core.DecreaseBonuses(user_number, value)
    await c.message.edit_text(text=f'Баллы сняты у {user_name}✅', reply_markup=admn_kb.get_menu())