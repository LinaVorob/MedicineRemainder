import os
from dataclasses import dataclass

from aiogram import Dispatcher
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

CATEGORIES = [
    'Антибактериальный препарат',
    'Антибиотик',
    'Гормоны',
    'Диагностическое средство',
    'Влияющее на иммунитет',
    'Влияющее на метаболизм',
    'Влияющее на психику',
    'Влияющее на свертываемость крови',
    'Сосудотонизирующее',
    'Сосудосуживающее',
    'Влияющее на функцию бронхов',
    'Влияющее на функции ЖКТ',
    'Влияющее на функции миокарда',
    'Влияющее на функцию почек',
    "Мочегонное",
    'Противовирусное',
    'Противовоспалительное',
    'Обезболивающее',
    'Противогрибковое',
    'Противоопухолевое',
    'Противопаразитарное',
    'Противоглистное'
]


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
        host=os.getenv('HOST')
    )
)
