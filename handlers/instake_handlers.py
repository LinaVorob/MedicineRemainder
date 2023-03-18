import datetime
from pprint import pprint

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.filters import OrFilter
from aiogram.types import CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, DialogCalendar, simple_cal_callback, dialog_cal_callback

from config import config
from keyboards.intake import keyboard_yes_no, calendar, keyboard_time_hour, keyboard_time_minute
from messages import MESSAGE_HAS_BREAK, DO_NOT_UNDERSTAND, MESSAGE_ONE_PERIOD, MESSAGE_COUNT_IN_DAY, MESSAGE_BREAK, \
    MESSAGE_TIME_STEP, MESSAGE_TIME, MESSAGE_DOZE, MESSAGE_DOZE_IN_PACKAGE, MESSAGE_MEDICINE_INTAKE_ADDED, \
    MESSAGE_CALENDAR, MESSAGE_TIME_STEP_RESULT, MESSAGE_TIME_RESULT
from validators import validator_digit
from utils import Time

time = Time()


async def switch_calendar(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    print(callback)
    print(callback_data)
    if callback_data['@'] == 'simple_calendar':
        obj = SimpleCalendar
    elif callback_data['@'] == 'dialog_calendar':
        obj = DialogCalendar
    else:
        raise AttributeError('Неизвестный тип календаря')
    await add_intake_common_period(callback, callback_data, state, obj)


async def add_intake_common_period(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext, obj):
    print(callback)
    print(callback_data)
    selected, date = await obj().process_selection(callback, callback_data)
    if selected:
        if selected:
            await state.set_data({'period': date})
            await state.set_state(config.state_input.is_break.state)
            await callback.message.edit_text(f'Выбрано:\n{date.day}.{date.month}.{date.year}')
            await callback.message.answer(MESSAGE_HAS_BREAK, reply_markup=keyboard_yes_no)
        else:
            await callback.message.answer(DO_NOT_UNDERSTAND)


async def add_to_intake_break(callback: CallbackQuery, state: FSMContext):
    answer = bool(int(callback.data))
    await state.set_data({'is_break': answer})
    if answer:
        await state.set_state(config.state_input.past_one_intake.state)
        await callback.message.answer(MESSAGE_ONE_PERIOD)
    else:
        await state.set_state(config.state_input.count_intakes_for_one_day.state)
        await callback.message.answer(MESSAGE_COUNT_IN_DAY)


async def add_duration_nonstop(message: Message, state: FSMContext):
    if validator_digit(message.text):
        await state.set_data({'past_one_intake': int(message.text)})
        await state.set_state(config.state_input.step_day_intake.state)
        await message.answer(MESSAGE_BREAK)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_duration_of_break(message: Message, state: FSMContext):
    if validator_digit(message.text):
        await state.set_data({'step_day_intake': int(message.text)})
        await state.set_state(config.state_input.count_intakes_for_one_day.state)
        await message.answer(MESSAGE_COUNT_IN_DAY)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_count_intakes_for_day(message: Message, state: FSMContext):
    if validator_digit(message.text):
        count = int(message.text)
        await state.set_data({'count_input_for_one_day': count})
        if count > 1:
            await state.set_state(config.state_input.between_in_day_hour.state)
            await message.answer(MESSAGE_TIME_STEP + '\n Укажите кол-во часов:', reply_markup=keyboard_time_hour)
        else:
            await state.set_state(config.state_input.time_intake_hour.state)
            await message.answer(MESSAGE_TIME + '\n Укажите час:', reply_markup=keyboard_time_hour)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def set_hour_between(callback: CallbackQuery, state: FSMContext):
    if validator_digit(callback.data):
        time.hour = int(callback.data)
        await state.set_state(config.state_input.between_in_day_minute.state)
        await callback.message.edit_text(MESSAGE_TIME_STEP + '\n Укажите кол-во минут:',
                                         reply_markup=keyboard_time_minute)
    else:
        await callback.message.answer(DO_NOT_UNDERSTAND)


async def set_minute_between(callback: CallbackQuery, state: FSMContext):
    if callback.data.isdigit():
        time.minute = int(callback.data)
        await state.set_data({'between_in_day': datetime.time(time.hour, time.minute)})
        await state.set_state(config.state_input.time_intake_hour.state)
        await callback.message.edit_text(MESSAGE_TIME_STEP_RESULT.format(time.hour, time.minute))
        await callback.message.answer(MESSAGE_TIME + '\n Укажите час:', reply_markup=keyboard_time_hour)
    else:
        await callback.message.answer(DO_NOT_UNDERSTAND)


async def set_hour_intake(callback: CallbackQuery, state: FSMContext):
    if validator_digit(callback.data):
        time.hour = int(callback.data)
        await state.set_state(config.state_input.time_intake_minute.state)
        await callback.message.edit_text(MESSAGE_TIME + '\n Укажите минуту:', reply_markup=keyboard_time_minute)
    else:
        await callback.message.answer(DO_NOT_UNDERSTAND)


async def set_minute_intake(callback: CallbackQuery, state: FSMContext):
    if callback.data.isdigit():
        time.minute = int(callback.data)
        await state.set_data({'time_intake': datetime.time(time.hour, time.minute)})
        await state.set_state(config.state_input.doze.state)
        await callback.message.edit_text(MESSAGE_TIME_RESULT.format(time.hour, time.minute))
        await callback.message.answer(MESSAGE_DOZE)
    else:
        await callback.message.answer(DO_NOT_UNDERSTAND)


async def add_count_doze_at_once(message: Message, state: FSMContext):
    if validator_digit(message.text):
        await state.set_data({'doze': int(message.text)})
        await state.set_state(config.state_input.doze_in_package.state)
        await message.answer(MESSAGE_DOZE_IN_PACKAGE)
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def add_count_doze_in_package(message: Message, state: FSMContext):
    if validator_digit(message.text):
        await state.set_data({'doze_in_package': int(message.text)})
        await state.finish()
        async with state.proxy() as data:
            name = data.get('name')
        await message.answer(MESSAGE_MEDICINE_INTAKE_ADDED.format(name))
    else:
        await message.answer(DO_NOT_UNDERSTAND)


async def write_intake(message: Message):
    pprint(message)
    answer_message = f"Приём лекарства {'s'} записано"
    await message.answer(answer_message)


async def get_info_about_intakes(message: Message):
    pprint(message)
    answer_message = f"Лекарство {'s'} изменено"
    await message.answer(answer_message)
    # if db.check_medicine()


async def nav_cal_handler(callback: CallbackQuery):
    await callback.message.answer(MESSAGE_CALENDAR, reply_markup=await SimpleCalendar().start_calendar())


async def simple_cal_handler(callback: CallbackQuery):
    await callback.message.answer(MESSAGE_CALENDAR, reply_markup=await DialogCalendar().start_calendar())


async def without_term(callback: CallbackQuery, state: FSMContext):
    await state.set_data({'period': None})
    await state.set_state(config.state_input.is_break.state)
    await callback.message.answer(MESSAGE_HAS_BREAK, reply_markup=keyboard_yes_no)


def register_intakes_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(switch_calendar,
                                       OrFilter(simple_cal_callback.filter(), dialog_cal_callback.filter()),
                                       state=config.state_input.period)
    dp.register_callback_query_handler(nav_cal_handler, calendar.filter(calendar_type='nav'),
                                       state=config.state_input.period)
    dp.register_callback_query_handler(simple_cal_handler, calendar.filter(calendar_type='dialog'),
                                       state=config.state_input.period)
    dp.register_callback_query_handler(without_term, calendar.filter(calendar_type='none'),
                                       state=config.state_input.period)
    dp.register_callback_query_handler(add_to_intake_break, state=config.state_input.is_break)
    dp.register_message_handler(add_duration_nonstop, state=config.state_input.past_one_intake)
    dp.register_message_handler(add_duration_of_break, state=config.state_input.step_day_intake)
    dp.register_message_handler(add_count_intakes_for_day, state=config.state_input.count_intakes_for_one_day)
    dp.register_callback_query_handler(set_hour_between, state=config.state_input.between_in_day_hour)
    dp.register_callback_query_handler(set_minute_between, state=config.state_input.between_in_day_minute)
    dp.register_callback_query_handler(set_hour_intake, state=config.state_input.time_intake_hour)
    dp.register_callback_query_handler(set_minute_intake, state=config.state_input.time_intake_minute)
    dp.register_message_handler(add_count_doze_at_once, state=config.state_input.doze)
    dp.register_message_handler(add_count_doze_in_package, state=config.state_input.doze_in_package)
    dp.register_message_handler(write_intake, commands='medicine_take')
    dp.register_message_handler(write_intake, commands='intake_info')
