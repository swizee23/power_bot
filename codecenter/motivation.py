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
                                button_thinking,
                                button_thinking_under,
                                button_thinking_first_add,
                                button_motivation,
                                button_motivation_first_add,
                                button_motivation_under,
                                button_woman)

from codecenter.functions import (mindset, mindmotiv, mindwoman)



router_motivation = Router()

class url_video2(StatesGroup):
    give_url2 = State()
    remark2 = State()

class InfoUrl2(CallbackData, prefix ="user"):
    action: str
    num_url: int


class change_url2(StatesGroup):
    n2 = State()
    url2 = State()
    under_note2 = State()



@router_motivation.message(F.text == "МОТИВАЦИЯ💰")
async def motivation(message, state: FSMContext):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS motivation1("
                           "number INTEGER PRIMARY KEY,"
                           "owner_id INTEGER,"
                           "url TEXT,"
                           "text TEXT)")
        await conn.commit()


    await message.answer("Выбери действие:",reply_markup=button_motivation())


@router_motivation.callback_query(lambda q: q.data == "show2")
async def show2(callback):
    current_user_id = callback.from_user.id
    info = await mindmotiv(user_id=current_user_id)

    if info:
        text_quote = "📌<b>Вот все ссылки:</b>\n\n"
        for number, url, text in info:
            text_quote += f"<b>{number}.</b> <b>Ссылка:</b> {url}\n\n<b>Примечание:</b>\n{text}\n\n\n"


        await callback.message.answer(text_quote,reply_markup=button_motivation_under(),parse_mode=ParseMode.HTML)
    else:
        await callback.message.answer("В файле пока пусто, добавь первую ссылку",reply_markup=button_motivation_first_add())


    await callback.answer()


@router_motivation.callback_query(lambda q: q.data == "delete2")
async def delete_2(callback):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("DELETE FROM motivation1 WHERE owner_id = ?",(callback.from_user.id,))
        await conn.commit()
    await callback.message.delete()
    await callback.message.answer("Все данные удаленны!")




@router_motivation.callback_query(lambda q: q.data == "add2")
async def add2(callback, state:FSMContext):
    await callback.message.answer("Отправь ссылку на видео")
    await state.set_state(url_video2.give_url2)


@router_motivation.callback_query(lambda q: q.data == "firstadd2")
async def first_add2(callback, state:FSMContext):
    await callback.message.answer("Отправь первую ссылку на видео")
    await state.set_state(url_video2.give_url2)


@router_motivation.message(url_video2.give_url2, F.text)
async def first_for_url2(message, state:FSMContext):
    #user_url = message.text
  #  if "h" or "." not in user_url:
   #     await message.answer("Введи ссылку!")
    #    return
    await state.update_data(give_url=message.text)
    await message.answer("Замечательно, теперь напиши примечание к видео")
    await state.set_state(url_video2.remark2)


@router_motivation.message(url_video2.remark2, F.text)
async def first_url_text2(message, state: FSMContext):

    await state.update_data(remark=message.text)

    data_info = await state.get_data()
    data_url = data_info.get("give_url")
    data_text = data_info.get("remark")
    first_id = message.from_user.id


    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("INSERT INTO motivation1 (owner_id, url, text) VALUES (?,?,?) ",(first_id,data_url,data_text))
        await conn.commit()
    await state.clear()
    await message.answer("Твое видео сохранено в МОТИВАЦИЯ",reply_markup=button_motivation())




@router_motivation.callback_query(lambda q: q.data == "change2")
async def change_2(callback, state: FSMContext):
    await callback.message.answer("Напишите число видео, которое вы хотите изменить")
    await state.set_state(change_url2.n2)


@router_motivation.message(change_url2.n2, F.text)
async def hello_number2(message, state:FSMContext):
    number_of_url = message.text

    if not number_of_url.isdigit():
       await message.answer("Введите число!")
       return

    await state.update_data(n=int(number_of_url))
    await state.set_state(change_url2.url2)
    await message.answer("Введите измененную ссылку")

@router_motivation.message(change_url2.url2, F.text)
async def update_url2(message: Message, state: FSMContext):
    upgrade_url = message.text
    await state.update_data(url=upgrade_url)
    await state.set_state(change_url2.under_note2)
    await message.answer("Введите новое описание к видео")



@router_motivation.message(change_url2.under_note2, F.text)
async def update_note2(message: Message, state: FSMContext):
    await state.update_data(under_note=message.text)

    all_data = await state.get_data()
    new_number = all_data.get("n")
    new_url = all_data.get("url")
    new_note = all_data.get("under_note")
    id = message.from_user.id

    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("UPDATE motivation1 SET url = ?, text = ? WHERE owner_id = ? AND number = ?", (new_url,new_note,id,new_number))
        await conn.commit()
    await message.answer("Ваше видео успешно изменено",reply_markup=button_motivation())
    await state.clear()