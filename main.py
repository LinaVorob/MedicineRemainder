import asyncio
from traceback import format_exc
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import config, set_main_menu
from handlers import register_users_handlers, register_intakes_handlers, register_medicines_handlers


def register_all_handlers(dp: Dispatcher):
    register_users_handlers(dp)
    register_intakes_handlers(dp)
    register_medicines_handlers(dp)


async def main():
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tgbot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp: Dispatcher = Dispatcher(bot, storage=storage)
    await set_main_menu(dp)

    # Регистрируем все хэндлеры
    register_all_handlers(dp)

    try:
        await dp.skip_updates()
        print('Start')
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Error!!!', format_exc())
