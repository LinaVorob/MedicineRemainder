import os
from dataclasses import dataclass

from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import BotCommand
from dotenv import load_dotenv

COMMAND = {
    '/add': "Добавить лекарство",
    '/medicine_take': "Записать приём лекарства",
    "/delete": "Удалить лекарство",
    "/info": "Информация о лекарстве",
    "/intake_info": "Информация о приеме лекарства",
    "/update": "Внести изменения в лекарство и/или его приём"
}

PATTERN = r'((\d{1,2})\s?(?:год|лет|года))?\s?((\d{1,2})\s?месяц(?:а|ев)?)?\s?((\d{1,2})\s?(?:день|дня|дней))?\s?(\d\d:\d\d:\d\d)?'
PATTERN_TIME_CLASSIC = r'(\d\d):(\d\d)'
PATTERN_TIME_WORDS = r'(\d{1,2}ч)\s?(\d{1,2}м)'

class InputForm(StatesGroup):
    # название лекарства
    name = State()
    # название категории
    category = State()
    # условия приема
    condition = State()
    # есть ли перерыв
    is_break = State()
    # общее время приема
    period = State()
    # длительность непрерывного приема
    past_one_intake = State()
    # кол-во приемов в день
    count_intakes_for_one_day = State()
    # время приема
    time_intake = State()
    # длительность перерыва
    step_day_intake = State()
    # время между приемами для одного дня
    between_in_day = State()
    doze = State()
    doze_in_package = State()


@dataclass
class DatabaseConfig:
    database: str
    user: str
    password: str
    host: str


@dataclass
class TgConfig:
    token: str
    admin_id: int


@dataclass
class Config:
    tgbot: TgConfig
    db: DatabaseConfig
    state_input: InputForm = InputForm()


async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in COMMAND.items()]
    await dp.bot.set_my_commands(main_menu_commands)


load_dotenv()

config = Config(
    tgbot=TgConfig(
        token=os.getenv("TOKEN"),
        admin_id=int(os.getenv('ADMIN'))),
    db=DatabaseConfig(
        database=os.getenv('DATABASE'),
        user=os.getenv('LOGIN'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
    )
)
