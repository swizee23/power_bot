import aiogram
from unittest import result
from aiogram.filters.callback_data import CallbackData
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command, Filter, callback_data
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton, FSInputFile, text_quote)
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
import aiohttp
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, types, html
import aiosqlite
from aiogram.filters.callback_data import CallbackData
import asyncio
import datetime as dt
from aiogram.enums import ParseMode, parse_mode
from aiogram.filters.callback_data import CallbackData
from codecenter.buttons import (button_group,
                                button_motivation,
                                button_motivation_first_add,
                                button_motivation_under,
                                button_woman,
                                button_woman_first_add,
                                button_woman_under)

from codecenter.functions import (mindset, mindmotiv, mindwoman)


router_woman = Router()


class url_video3(StatesGroup):
    give_url3 = State()
    remark3 = State()

class InfoUrl3(CallbackData, prefix ="user"):
    action: str
    num_url: int


class change_url3(StatesGroup):
    n3 = State()
    url3 = State()
    under_note3 = State()



@router_woman.message(F.text == "ЖЕНЩИНЫ👙")
async def motivation(message, state: FSMContext):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS woman1("
                           "number INTEGER PRIMARY KEY,"
                           "owner_id INTEGER,"
                           "url TEXT,"
                           "text TEXT)")
        await conn.commit()


    await message.answer("Выбери действие:",reply_markup=button_woman())


@router_woman.callback_query(lambda q: q.data == "show3")
async def show3(callback):
    current_user_id = callback.from_user.id
    info = await mindwoman(owner_id=current_user_id)

    if info:
        text_quote = "📌<b>Вот все ссылки:</b>\n\n"
        for number, url, text in info:
            text_quote += f"<b>{number}.</b> <b>Ссылка:</b> {url}\n\n<b>Примечание:</b>\n{text}\n\n\n"

        await callback.message.answer(text_quote,reply_markup=button_woman_under(),parse_mode=ParseMode.HTML)
    else:
        await callback.message.answer("В файле пока пусто, добавь первую ссылку",reply_markup=button_woman_first_add())


    await callback.answer()


@router_woman.callback_query(lambda q: q.data == "delete3")
async def delete_3(callback):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("DELETE FROM woman1 WHERE owner_id = ?",(callback.from_user.id,))
        await conn.commit()
    await callback.message.delete()
    await callback.message.answer("Все данные удаленны!")




@router_woman.callback_query(lambda q: q.data == "add3")
async def add2(callback, state:FSMContext):
    await callback.message.answer("Отправь ссылку на видео")
    await state.set_state(url_video3.give_url3)


@router_woman.callback_query(lambda q: q.data == "firstadd3")
async def first_add2(callback, state:FSMContext):
    await callback.message.answer("Отправь первую ссылку на видео")
    await state.set_state(url_video3.give_url3)


@router_woman.message(url_video3.give_url3, F.text)
async def first_for_url3(message, state:FSMContext):
    #user_url = message.text
  #  if "h" or "." not in user_url:
   #     await message.answer("Введи ссылку!")
    #    return
    await state.update_data(give_url=message.text)
    await message.answer("Замечательно, теперь напиши примечание к видео")
    await state.set_state(url_video3.remark3)


@router_woman.message(url_video3.remark3, F.text)
async def first_url_text3(message, state: FSMContext):

    await state.update_data(remark=message.text)

    data_info = await state.get_data()
    data_url = data_info.get("give_url")
    data_text = data_info.get("remark")
    first_id = message.from_user.id


    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("INSERT INTO woman1 (owner_id, url, text) VALUES (?,?,?) ",(first_id,data_url,data_text))
        await conn.commit()
    await state.clear()
    await message.answer("Твое видео сохранено в ЖЕНЩИНЫ",reply_markup=button_woman())




@router_woman.callback_query(lambda q: q.data == "change3")
async def change_3(callback, state: FSMContext):
    await callback.message.answer("Напишите число видео, которое вы хотите изменить")
    await state.set_state(change_url3.n3)


@router_woman.message(change_url3.n3, F.text)
async def hello_number3(message, state:FSMContext):
    number_of_url = message.text

    if not number_of_url.isdigit():
       await message.answer("Введите число!")
       return

    await state.update_data(n=int(number_of_url))
    await state.set_state(change_url3.url3)
    await message.answer("Введите измененную ссылку")

@router_woman.message(change_url3.url3, F.text)
async def update_url3(message: Message, state: FSMContext):
    upgrade_url = message.text
    await state.update_data(url=upgrade_url)
    await state.set_state(change_url3.under_note3)
    await message.answer("Введите новое описание к видео")



@router_woman.message(change_url3.under_note3, F.text)
async def update_note3(message: Message, state: FSMContext):
    await state.update_data(under_note=message.text)

    all_data = await state.get_data()
    new_number = all_data.get("n")
    new_url = all_data.get("url")
    new_note = all_data.get("under_note")
    id = message.from_user.id

    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("UPDATE woman1 SET url = ?, text = ? WHERE owner_id = ? AND number = ?", (new_url,new_note,id,new_number))
        await conn.commit()
    await message.answer("Ваше видео успешно изменено",reply_markup=button_woman())
    await state.clear()