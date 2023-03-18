from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config import config
from db.core import Database
from entities import MedicineType
from keyboards.intake import keyboard_calendar
from keyboards.medicine import keyboard_category
from messages import MESSAGE_GET_NAME, MESSAGE_GET_CATEGORY, MESSAGE_COMMON_PERIOD, MESSAGE_GET_CONDITION_OF_INTAKE

db_ins = Database()


async def add_medicine(message: types.Message, state: FSMContext):
    pprint(message)
    await state.set_state(config.state_input.name.state)
    await message.answer(MESSAGE_GET_NAME)


async def update_medicine(message: types.Message):
    pprint(message)
    answer_message = f"Лекарство {'s'} изменено"
    await message.answer(answer_message)


async def get_info_about_medicine(message: types.Message):
    pprint(message)
    answer_message = f" Это лекарство называется {'s'}"
    await message.answer(answer_message)


async def delete_medicine(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    pprint(message)
    answer_message = f"Лекарство {'s'} удалено"
    await message.answer(answer_message)


async def adding_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Добавление лекарства отменено")


async def add_medicine_name(message: types.Message, state: FSMContext):
    await state.set_data({'name': message.text})
    if not db_ins.check_medicine('medicine_name', message.text):
        medicine = MedicineType(name=message.text)
        async with state.proxy() as data:
            data['name'] = medicine  # TODO допилить
        await state.set_state(config.state_input.category.state)
        await message.answer(MESSAGE_GET_CATEGORY, reply_markup=keyboard_category)
    else:
        await state.set_state(config.state_input.period.state)
        await message.answer(MESSAGE_COMMON_PERIOD, reply_markup=keyboard_calendar)


async def add_medicine_category(callback: CallbackQuery, state: FSMContext):
    await state.set_data({'category': callback.data})
    await state.set_state(config.state_input.condition.state)
    await callback.message.answer(MESSAGE_GET_CONDITION_OF_INTAKE)


async def add_condition_intake(message: types.Message, state: FSMContext):
    await state.set_data({'condition': message.text})
    await state.set_state(config.state_input.period.state)
    await message.answer(MESSAGE_COMMON_PERIOD, reply_markup=keyboard_calendar)


def register_medicines_handlers(dp: Dispatcher):
    dp.register_message_handler(add_medicine, commands='add', state='*')
    dp.register_message_handler(adding_cancel, commands="cancel", state="*")
    dp.register_message_handler(update_medicine, commands='update')
    dp.register_message_handler(get_info_about_medicine, commands='info')
    dp.register_message_handler(delete_medicine, commands='delete')
    dp.register_message_handler(add_medicine_name, state=config.state_input.name)
    dp.register_callback_query_handler(add_medicine_category, state=config.state_input.category)
    dp.register_message_handler(add_condition_intake, state=config.state_input.condition)
