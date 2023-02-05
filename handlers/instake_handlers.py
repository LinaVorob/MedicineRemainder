from pprint import pprint

from aiogram import types, Dispatcher


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
    dp.register_message_handler(write_intake, commands='medicine_take')
    dp.register_message_handler(write_intake, commands='intake_info')