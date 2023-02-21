from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config import config
from keyboards.intake import keyboard_break
from messages import MESSAGE_HAS_BREAK, DO_NOT_UNDERSTAND, MESSAGE_ONE_PERIOD, MESSAGE_COUNT_IN_DAY, MESSAGE_BREAK, \
    MESSAGE_TIME_STEP, MESSAGE_TIME, MESSAGE_DOZE, MESSAGE_DOZE_IN_PACKAGE, MESSAGE_MEDICINE_INTAKE_ADDED
from utils import convert_to_datetime
from validators import date_format_validator, validator_digit, validator_time


async def add_intake_common_period(message: types.Message, state: FSMContext):
    await state.update_data(period=message.text)
    if date_format_validator(message.text):
        date = convert_to_datetime(message.text)
        await state.update_data(period=date)
        await state.set_state(config.state_input.is_break.state)
        await message.answer(MESSAGE_HAS_BREAK, reply_markup=keyboard_break)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_to_intake_break(callback: CallbackQuery, state: FSMContext):
    answer = bool(int(callback.data))
    await state.update_data(is_break=answer)
    if answer:
        await state.set_state(config.state_input.past_one_intake.state)
        await callback.answer(MESSAGE_ONE_PERIOD)
    else:
        await state.set_state(config.state_input.count_intakes_for_one_day.state)
        await callback.answer(MESSAGE_COUNT_IN_DAY)


async def add_duration_nonstop(message: types.Message, state: FSMContext):
    if validator_digit(message.text):
        await state.update_data(past_one_intake=int(message.text))
        await state.set_state(config.state_input.step_day_intake.state)
        await message.answer(MESSAGE_BREAK)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_duration_of_break(message: types.Message, state: FSMContext):
    if validator_digit(message.text):
        await state.update_data(step_day_intake=int(message.text))
        await state.set_state(config.state_input.count_intakes_for_one_day.state)
        await message.answer(MESSAGE_COUNT_IN_DAY)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_count_intakes_for_day(message: types.Message, state: FSMContext):
    if validator_digit(message.text):
        count = int(message.text)
        await state.update_data(count_input_for_one_day=count)
        if count > 2:
            await state.set_state(config.state_input.between_in_day.state)
            await message.answer(MESSAGE_TIME_STEP)
        else:
            await state.set_state(config.state_input.time_intake.state)
            await message.answer(MESSAGE_TIME)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_time_between(message: types.Message, state: FSMContext):
    if validator_time(message.text):
        await state.update_data(between_in_day=message.text)
        await state.set_state(config.state_input.time_intake.state)
        await message.answer(MESSAGE_TIME)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_time_intake(message: types.Message, state: FSMContext):
    if validator_time(message.text):
        await state.update_data(time_intake=message.text)
        await state.set_state(config.state_input.doze.state)
        await message.answer(MESSAGE_DOZE)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_count_doze_at_once(message: types.Message, state: FSMContext):
    if validator_digit(message.text):
        await state.update_data(doze=int(message.text))
        await state.set_state(config.state_input.doze_in_package.state)
        await message.answer(MESSAGE_DOZE_IN_PACKAGE)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_count_doze_in_package(message: types.Message, state: FSMContext):
    if validator_digit(message.text):
        await state.update_data(doze_in_package=int(message.text))
        await state.finish()
        await message.answer(MESSAGE_MEDICINE_INTAKE_ADDED.format(await state.get_data('name')))
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def write_intake(message: types.Message):
    pprint(message)
    answer_message = f"Приём лекарства {'s'} записано"
    await message.answer(answer_message)


async def get_info_about_intakes(message: types.Message):
    pprint(message)
    answer_message = f"Лекарство {'s'} изменено"
    await message.answer(answer_message)
    # if db.check_medicine()


def register_intakes_handlers(dp: Dispatcher):
    dp.register_message_handler(add_intake_common_period, state=config.state_input.period)
    dp.register_callback_query_handler(add_to_intake_break, state=config.state_input.is_break)
    dp.register_message_handler(add_duration_nonstop, state=config.state_input.past_one_intake)
    dp.register_message_handler(add_duration_of_break, state=config.state_input.step_day_intake)
    dp.register_message_handler(add_count_intakes_for_day, state=config.state_input.count_intakes_for_one_day)
    dp.register_message_handler(add_time_between, state=config.state_input.between_in_day)
    dp.register_message_handler(add_time_intake, state=config.state_input.time_intake)
    dp.register_message_handler(add_count_doze_at_once, state=config.state_input.doze)
    dp.register_message_handler(add_count_doze_in_package, state=config.state_input.doze_in_package)
    dp.register_message_handler(write_intake, commands='medicine_take')
    dp.register_message_handler(write_intake, commands='intake_info')
