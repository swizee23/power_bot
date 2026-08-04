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
                                button_woman)

from codecenter.functions import (mindset, mindmotiv, mindwoman)

db = "database.db"
router = Router()

class url_video(StatesGroup):
    give_url = State()
    remark = State()

class InfoUrl(CallbackData, prefix ="user"):
    action: str
    num_url: int



class change_url(StatesGroup):
    n = State()
    url = State()
    under_note = State()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Этот бот - это уголок силы и разума в интернете")
    await message.answer("Здесь будет храниться самая нужная информация, чтобы я не забывал направление")
    await message.answer("Нажми на /continue чтобы продолжить")
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS thinking1("
                           "number INTEGER PRIMARY KEY,"
                           "owner_id INTEGER,"
                           "url TEXT,"
                           "text TEXT)")

        await conn.commit()

    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS motivation("
                           "id INTEGER,"
                           "number INTEGER PRIMARY KEY,"
                           "url TEXT,"
                           "text TEXT)")
        await conn.commit()

    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS woman("
                           "id INTEGER,"
                           "number INTEGER PRIMARY KEY,"
                           "url TEXT,"
                           "text TEXT)")
        await conn.commit()



@router.message(Command("continue"))
async def next(message: Message):
    await message.answer("Замечательно, выбери группу с которой будешь взаимодействовать",reply_markup=button_group())

@router.message(F.text == "Мышление")
async def mind(message, state: FSMContext):


    await message.answer("Выбери действие:",reply_markup=button_thinking())


@router.callback_query(lambda q: q.data == "show1")
async def show1(callback):
    current_user_id = callback.from_user.id
    info = await mindset(owner_id=current_user_id)

    if info:
        text_quote = "Вот все ссылки:\n\n"
        for number, url, text in info:
            text_quote += f"{number}. Ссылка: {url}\nПримечание: {text}\n\n"

        await callback.message.answer(text_quote,reply_markup=button_thinking_under())
    else:
        await callback.message.answer("В файле пока пусто, добавь первую ссылку",reply_markup=button_thinking_first_add())


    await callback.answer()


@router.callback_query(lambda q: q.data == "delete1")
async def delete_1(callback):
    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("DELETE FROM thinking1 WHERE owner_id = ?",(callback.from_user.id,))
        await conn.commit()
    await callback.message.delete()
    await callback.message.answer("Все данные удаленны!")




@router.callback_query(lambda q: q.data == "add1")
async def add1(callback, state:FSMContext):
    await callback.message.answer("Отправь ссылку на видео")
    await state.set_state(url_video.give_url)


@router.callback_query(lambda q: q.data == "firstadd")
async def first_add1(callback, state:FSMContext):
    await callback.message.answer("Отправь первую ссылку на видео")
    await state.set_state(url_video.give_url)


@router.message(url_video.give_url, F.text)
async def first_for_url(message, state:FSMContext):
    #user_url = message.text
  #  if "h" or "." not in user_url:
   #     await message.answer("Введи ссылку!")
    #    return
    await state.update_data(give_url=message.text)
    await message.answer("Замечательно, теперь напиши примечание к видео")
    await state.set_state(url_video.remark)


@router.message(url_video.remark, F.text)
async def first_url_text(message, state: FSMContext):

    await state.update_data(remark=message.text)

    data_info = await state.get_data()
    data_url = data_info.get("give_url")
    data_text = data_info.get("remark")
    first_id = message.from_user.id


    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("INSERT INTO thinking1 (owner_id, url, text) VALUES (?,?,?) ",(first_id,data_url,data_text))
        await conn.commit()
    await state.clear()
    await message.answer("Твое видео сохранено в МЫШЛЕНИЕ")







@router.callback_query(lambda q: q.data == "change1")
async def change_1(callback, state: FSMContext):
    await callback.message.answer("Напишите число видео, которое вы хотите изменить")
    await state.set_state(change_url.n)


@router.message(change_url.n, F.text)
async def hello_number(message, state:FSMContext):
    number_of_url = message.text

    if not number_of_url.isdigit():
       await message.answer("Введите число!")
       return

    await state.update_data(n=int(number_of_url))
    await state.set_state(change_url.url)
    await message.answer("Введите измененную ссылку")

@router.message(change_url.url, F.text)
async def update_url(message: Message, state: FSMContext):
    upgrade_url = message.text
    await state.update_data(url=upgrade_url)
    await state.set_state(change_url.under_note)
    await message.answer("Введите новое описание к видео")



@router.message(change_url.under_note, F.text)
async def update_note(message: Message, state: FSMContext):
    await state.update_data(under_note=message.text)

    all_data = await state.get_data()
    new_number = all_data.get("n")
    new_url = all_data.get("url")
    new_note = all_data.get("under_note")
    id = message.from_user.id

    async with aiosqlite.connect("database.db") as conn:
        await conn.execute("UPDATE thinking1 SET url = ?, text = ? WHERE owner_id = ? AND number = ?", (new_url,new_note,id,new_number))
        await conn.commit()
    await message.answer("Ваше видео успешно изменено",reply_markup=button_thinking())
    await state.clear()


