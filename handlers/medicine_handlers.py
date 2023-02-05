from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from db.core import Database
from messages import MESSAGE_GET_NAME, MESSAGE_ADDING_COMPLETED, MESSAGE_GET_CATEGORY, MESSAGE_COMMON_PERIOD

db_ins = Database()


class MedicineForm(StatesGroup):
    name = State()
    category = State()
    condition = State()
    is_break = State()
    period = State()
    past_one_intake = State()
    count_intakes_for_one_day = State()
    time_intake = State()
    step_day_intake = State()
    doze = State()
    doze_in_package = State()


async def add_medicine(message: types.Message, state: FSMContext):
    pprint(message)
    await state.set_state(MedicineForm.name.state)
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
    await state.update_data(name=message.text)
    if not db_ins.check_medicine('medicine_name', message.text):
        await state.set_state(MedicineForm.category.state)
        await message.answer(MESSAGE_GET_CATEGORY)
    else:
        await state.set_state(MedicineForm.period.state)
        await message.answer(MESSAGE_COMMON_PERIOD.format(message.text))


def register_medicines_handlers(dp: Dispatcher):
    dp.register_message_handler(add_medicine, commands='add', state='*')
    dp.register_message_handler(adding_cancel, commands="cancel", state="*")
    dp.register_message_handler(update_medicine, commands='update')
    dp.register_message_handler(get_info_about_medicine, commands='info')
    dp.register_message_handler(delete_medicine, commands='delete')
    dp.register_message_handler(add_medicine_name, state=MedicineForm.name)
