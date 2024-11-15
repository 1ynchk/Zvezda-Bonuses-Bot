from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from keyboards import admin_keyboards as admn_kb
from States.State import ClientStateGroup

pagination_router = Router()

async def make_caption_users(res, statement):
    cnt = 0
    numb = 0
    dictionary = {}
    str_stuff = ""
    values_stuff = []
    for i in range(len(res)):
        cnt += 1
        numb += 1
        if statement == 'Clients':
            nickname = res[i][0] + ' ' + res[i][1]
        else:
            nickname = res[i][0]
        if statement == 'Moderators':
            values_stuff.append((nickname, res[i][1]))
        else:
            values_stuff.append((res[i][0], res[i][1], res[i][2], res[i][3], res[i][4]))
        str_stuff += f"{f'{numb}){nickname}':<27}\n"

        if str_stuff.count("\n") < 11:
            separator = '-' * 33
            if cnt % 10 == 0:
                numb = 0
                dictionary[f"{cnt // 10}"] = [
                    {"str_stuff": "```" + f"\n{'Никнейм':<30}\n{separator}\n {str_stuff} ```",
                    "values_stuff": values_stuff}]
                str_stuff = ""

            else:
                dictionary[f"{cnt // 10 + 1}"] = [
                    {"str_stuff": "```" + f"\n{'Никнейм':<30}\n{separator}\n {str_stuff} ```",
                    "values_stuff": values_stuff}]
    
    cnt_stuff = dictionary["1"][0]["str_stuff"].count("\n") - 3
    keyboard = admn_kb.get_users(cnt_stuff, "1", statement)
    if len(dictionary.keys()) > 1:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=">>", callback_data="next_a")])
  
    return (dictionary, keyboard)

async def pagination_admin(state):
        
        data = await state.get_data()
        current_page = int(data.get("current_page"))
        dictionary = data.get("dictionary")
        statement = data.get("statement")
        cnt_user = dictionary[str(current_page)][0]["str_stuff"].count("\n") - 3
        keyboard = admn_kb.get_users(cnt_user, current_page, statement)
        
        if current_page == 1:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=">>", callback_data="next_a")])
            info = dictionary[str(current_page)][0]["str_stuff"]
            return (keyboard, info)
        
        elif current_page == len(dictionary.keys()):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text="<<", callback_data="back_a")])
            info = dictionary[str(current_page)][0]["str_stuff"]
            return (keyboard, info)
        
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text="<<", callback_data="back_a"), 
                                             InlineKeyboardButton(text=">>", callback_data="next_a")])
            info = dictionary[str(current_page)][0]["str_stuff"]
            return (keyboard, info)

@pagination_router.callback_query(F.data == "next_a", ClientStateGroup.pagination)
async def CALLnext_a(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get("current_page")
    await state.update_data(current_page=current_page+1)
    keyboard, info = await pagination_admin(state)

    await c.message.edit_text(text=info, 
                              reply_markup=keyboard,
                              parse_mode="MARKDOWN")


@pagination_router.callback_query(F.data == "back_a", ClientStateGroup.pagination)
async def CALLback_a(c: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get("current_page")
    photo_path = data.get("photo_path")
    await state.update_data(current_page=current_page-1)
    keyboard, info = await pagination_admin(state)

    await c.message.edit_text(text=info, 
                              reply_markup=keyboard,
                              parse_mode="MARKDOWN")