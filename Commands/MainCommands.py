from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import os
from dotenv import load_dotenv
from keyboards import admin_keyboards as admn_kb
from keyboards import moderator_keyboards as mdrt_kb
from Data.types.core import Core

load_dotenv()

mainCommands = Router()

@mainCommands.message(Command('start'))
async def Start(m: types.Message):
    pass

@mainCommands.message(Command('admin'))
async def Admin(m: types.Message, state: FSMContext):
    await state.clear()
    if int(m.from_user.id) == int(os.getenv('ADMIN')):
        await m.answer(text='➕➕➕➕ Админ панель ➕➕➕➕', reply_markup=admn_kb.admin_panel())
    else:
        await m.answer(text='У вас не хватает прав на админ панель', reply_markup=mdrt_kb.moderator_panel())

@mainCommands.callback_query(F.data == 'admin_panel')
async def Admin(c: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if int(c.from_user.id) == int(os.getenv('ADMIN')):
        await c.message.edit_text(text='➕➕➕➕ Админ панель ➕➕➕➕', reply_markup=admn_kb.admin_panel())
    else:
        await c.answer(text='У вас не хватает прав на админ панель', reply_markup=mdrt_kb.moderator_panel())

@mainCommands.message(Command('moderator'))
async def Admin(m: types.Message, state: FSMContext):
    moderators = await Core.GetAllModeratorsView()

    await state.clear()
    if int(m.from_user.id) == int(os.getenv('ADMIN')) or int(m.from_user.username) in moderators:
        await m.answer(text='➕➕➕➕ Панель модератора ➕➕➕➕', reply_markup=mdrt_kb.moderator_panel())

@mainCommands.callback_query(F.data == 'moder_panel')
async def Admin(c: types.CallbackQuery, state: FSMContext):
    moderators = await Core.GetAllModeratorsView()

    await state.clear()
    if int(c.from_user.id) == int(os.getenv('ADMIN')) or int(m.from_user.username) in moderators:
        await c.message.edit_text(text='➕➕➕➕ Панель модератора ➕➕➕➕', reply_markup=mdrt_kb.moderator_panel())