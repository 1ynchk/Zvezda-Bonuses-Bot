from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import os
from dotenv import load_dotenv
from keyboards import admin_keyboards as admn_kb

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

@mainCommands.callback_query(F.data == 'admin_panel')
async def Admin(c: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if int(c.from_user.id) == int(os.getenv('ADMIN')):
        await c.message.edit_text(text='Админ панель', reply_markup=admn_kb.admin_panel())