from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def moderator_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить клиента', callback_data='moder_create_client')],
        [InlineKeyboardButton(text='Найти клиента', callback_data='moder_find_client')],
    ])

def get_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='В меню', callback_data='moder_panel')]
    ])

def confirm_crating_client():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_crating_client')],
        [InlineKeyboardButton(text='Нет', callback_data='moder_panel')],
    ])