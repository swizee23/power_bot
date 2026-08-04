import aiogram
from unittest import result
from aiogram.filters.callback_data import CallbackData
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command, Filter, callback_data
from aiogram.types import (Message,InlineKeyboardMarkup, InlineKeyboardButton,
                     ReplyKeyboardMarkup,KeyboardButton, FSInputFile)
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


async def mindset(owner_id: int):
    async with aiosqlite.connect("database.db") as conn:
        async with conn.execute("SELECT number, url, text FROM thinking1 WHERE owner_id = ?",(owner_id,)) as cursor:
            result = await cursor.fetchall()
            return result


async def mindmotiv(user_id: int):
    async with aiosqlite.connect("database.db") as conn:
        async with conn.execute("SELECT number, url, text FROM motivation1 WHERE owner_id = ?",(user_id,)) as cursor:
            result = await cursor.fetchall()
            return result


async def mindwoman(owner_id: int):
    async with aiosqlite.connect("database.db") as conn:
        cursor = await conn.execute("SELECT number, url, text FROM woman1 WHERE owner_id = ?",(owner_id,))
        result = await cursor.fetchall()
        return result


