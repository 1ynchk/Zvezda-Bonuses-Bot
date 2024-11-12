from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from Data.types.core import Core
from keyboards import admin_keyboards as admn_kb
from Common import pagination as pag
from States.State import ClientStateGroup

import pprint

AdminCallbackRouter = Router()

@AdminCallbackRouter.callback_query(F.data == 'admin_moderators')
async def ModeratorsList(c: CallbackQuery, state: FSMContext):
    res = await Core.GetAllModerators() 

    if res == None or len(res) == 0:
        await c.message.edit_text(text="Модераторов еще нет",reply_markup=admn_kb.get_menu())
    else:
        dictionary, keyboard = await pag.make_caption_users(res)
        await c.message.edit_text(text=dictionary["1"][0]["str_stuff"], reply_markup=keyboard, parse_mode="MarkDownV2")

        await state.set_state(ClientStateGroup.pagination)
        await state.update_data(dictionary=dictionary, current_page=1, statement="Users")

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
    res = await Core.GetAllModerators() 

    if res == None or len(res) == 0:
        await c.message.edit_text(text="Клиентов еще нет",reply_markup=admn_kb.get_menu())
    else:
        dictionary, keyboard = await pag.make_caption_users(res)
        await c.message.edit_text(text=dictionary["1"][0]["str_stuff"], reply_markup=keyboard, parse_mode="MarkDownV2")

        await state.set_state(ClientStateGroup.pagination)
        await state.update_data(dictionary=dictionary, current_page=1, statement="Users")