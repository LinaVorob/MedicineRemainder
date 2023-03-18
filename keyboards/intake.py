from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def insert_digit_buttons(kb: InlineKeyboardMarkup, period: int, step: int):
    for item in range(0, period, step):
        button: InlineKeyboardButton = InlineKeyboardButton(
            text=str(item),
            callback_data=str(item))
        kb.insert(button)


calendar = CallbackData('NAV', 'calendar_type')
keyboard_yes_no: InlineKeyboardMarkup = InlineKeyboardMarkup()

# Создаем объекты инлайн-кнопок
button_yes: InlineKeyboardButton = InlineKeyboardButton(
    text='Да',
    callback_data='1')
button_no: InlineKeyboardButton = InlineKeyboardButton(
    text='Нет',
    callback_data='0')

keyboard_yes_no.add(button_yes).add(button_no)

keyboard_date = InlineKeyboardMarkup()

keyboard_calendar = InlineKeyboardMarkup(resize_keyboard=True)
button_nav = InlineKeyboardButton(text='Навигационный календарь', callback_data=calendar.new(calendar_type='nav'))
button_dialog = InlineKeyboardButton(text='Пошаговый календарь', callback_data=calendar.new(calendar_type='dialog'))
button_none = InlineKeyboardButton(text='Бессрочно', callback_data=calendar.new(calendar_type='none'))
keyboard_calendar.add(button_nav).add(button_dialog).add(button_none)

keyboard_time_hour = InlineKeyboardMarkup(row_width=5)
keyboard_time_minute = InlineKeyboardMarkup(row_width=5)

insert_digit_buttons(keyboard_time_hour, 24, 1)
insert_digit_buttons(keyboard_time_minute, 60, 5)
