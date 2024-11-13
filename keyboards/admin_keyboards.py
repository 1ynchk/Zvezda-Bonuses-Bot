from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Модераторы', callback_data='admin_moderators'),
         InlineKeyboardButton(text='Пользователи', callback_data='admin_clients')
        ],
        [InlineKeyboardButton(text='Добавить модератора', callback_data='admin_add_moderator')]
    ])

def get_users(cnt_users, sheet, statement):
    btns = []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Меню 📨", callback_data="admin_panel")],])
    for i in range(cnt_users):
        if i <= 4:
            btns.append(InlineKeyboardButton(text=f"{i+1}", callback_data=f"{'moderator' if statement=='Moderators' else 'client'}_{i+1}_{sheet}"))

        elif i == 5:
            keyboard.inline_keyboard.append(btns)
            btns = []
            btns.append(InlineKeyboardButton(text=f"{i+1}", callback_data=f"{'moderator' if statement=='Moderators' else 'client'}_{i+1}_{sheet}"))

        else:
            btns.append(InlineKeyboardButton(text=f"{i+1}", callback_data=f"{'moderator' if statement=='Moderators' else 'client'}_{i+1}_{sheet}"))

    keyboard.inline_keyboard.append(btns)

    return keyboard

def get_menu_client():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад⬅', callback_data='admin_clients')],
        [InlineKeyboardButton(text='Удалить❌', callback_data='admin_delete_client')],
        [InlineKeyboardButton(text='Начислить бонусы➕', callback_data='increase_bonuses')],
        [InlineKeyboardButton(text='Снять бонусы➖', callback_data='decrease_bonuses')]
    ])

def get_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Меню📨', callback_data='admin_panel')]
    ])

def confirm_blocking_moderator():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_blocking_moderator'),
         InlineKeyboardButton(text='Нет', callback_data='admin_moderators')]
    ])

def confirm_blocking_client():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_blocking_client'),
         InlineKeyboardButton(text='Нет', callback_data='admin_clients')]
    ])

def confirm_creating_moderator():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_creating_moderator'),
         InlineKeyboardButton(text='Нет', callback_data='admin_panel')]
    ])

def confirm_increasing_bonuses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_increasing_bonuses_moder'),
         InlineKeyboardButton(text='Нет', callback_data='admin_panel')]
    ])

def confirm_decreasing_bonuses():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='confirm_decreasing_bonuses'),
         InlineKeyboardButton(text='Нет', callback_data='admin_panel')]
    ])