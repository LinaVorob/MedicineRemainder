import os
import logging
from pprint import pprint

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import requests
from settings import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот, никогда не забывающий о лекарствах :)\n\n"
        "Добавить лекарство: /add\n"
        "Записать приём лекарства: /medicine_take\n"
        "Удалить лекарство: /delete\n"
        "Информация о лекарстве: /info\n"
        "Внести изменения в лекарство и/или его прим: /update\n")


@dp.message_handler(commands=['add'])
async def add_medicine(message: types.Message):
    """Добавляет лекарство в БД, если его там не было, и добавляет в расписание приема для пользователя"""
    pprint(message.text.split(' ')[-1])
    answer_message = f"Лекарство {'s'} добавлено"
    await message.answer(answer_message)


@dp.message_handler(commands=['medicine_take'])
async def write_intake(message: types.Message):
    pprint(message)
    answer_message = f"Приём лекарства {'s'} записано"
    await message.answer(answer_message)


@dp.message_handler(commands=['delete'])
async def delete_medicine(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    pprint(message)
    answer_message = f"Лекарство {'s'} удалено"
    await message.answer(answer_message)


@dp.message_handler(commands=['info'])
async def get_info_about_medicine(message: types.Message):
    pprint(message)
    answer_message = f" Это лекарство называется {'s'}"
    await message.answer(answer_message)


@dp.message_handler(commands=['update'])
async def update_medicine(message: types.Message):
    pprint(message)
    answer_message = f"Лекарство {'s'} изменено"
    await message.answer(answer_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
