from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_break: InlineKeyboardMarkup = InlineKeyboardMarkup()

# Создаем объекты инлайн-кнопок
button_yes: InlineKeyboardButton = InlineKeyboardButton(
                                        text='Да',
                                        callback_data='1')
button_no: InlineKeyboardButton = InlineKeyboardButton(
                                        text='Нет',
                                        callback_data='0')

keyboard_break.add(button_yes).add(button_no)