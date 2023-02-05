from aiogram import types, Dispatcher

from db.core import Database
from entities import UserType
from messages import MESSAGE_HELP, MESSAGE_START

db = Database()


async def send_help(message: types.Message):
    """Отправляет помощь по боту"""
    await message.answer(MESSAGE_HELP)


async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""

    user = UserType.parse_obj(message.from_user)

    if not db.check_user(param='user_id_telegram', value_check=user.tg_id):
        db.add_new_user(user)
    await message.answer(MESSAGE_START)


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(send_help, commands='help')
