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

def button_group():
    button = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="МЫШЛЕНИЕ🧠")],
            [KeyboardButton(text="МОТИВАЦИЯ💰")],
            [KeyboardButton(text="ЖЕНЩИНЫ👙")]
        ],
        resize_keyboard=True
    )
    return button





def button_thinking():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ПОСМОТРЕТЬ🔍",callback_data="show1")]
        ]
    )
    return button


def button_thinking_under():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="add1")],
            [InlineKeyboardButton(text="ИЗМЕНИТЬ♻️",callback_data="change1")],
            [InlineKeyboardButton(text="УДАЛИТЬ🗑️", callback_data="delete1")]
        ]
    )
    return button

def button_thinking_first_add():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="firstadd")]
        ]
    )
    return button









def button_motivation():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ПОСМОТРЕТЬ🔍",callback_data="show2")],

        ]
    )
    return button

def button_motivation_under():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="add2")],
            [InlineKeyboardButton(text="ИЗМЕНИТЬ♻️",callback_data="change2")],
            [InlineKeyboardButton(text="УДАЛИТЬ🗑️", callback_data="delete2")]
        ]
    )
    return button

def button_motivation_first_add():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="firstadd2")]
        ]
    )
    return button








def button_woman():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ПОСМОТРЕТЬ🔍",callback_data="show3")],
        ]
    )
    return button


def button_woman_under():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="add3")],
            [InlineKeyboardButton(text="ИЗМЕНИТЬ♻️",callback_data="change3")],
            [InlineKeyboardButton(text="УДАЛИТЬ🗑️", callback_data="delete3")]
        ]
    )
    return button

def button_woman_first_add():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ДОБАВИТЬ✅",callback_data="firstadd3")]
        ]
    )
    return button