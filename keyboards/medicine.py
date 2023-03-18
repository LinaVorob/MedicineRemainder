from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.core import Database

keyboard_category = InlineKeyboardMarkup(row_width=2)

db = Database()
categories = db.get_categories()
for category in categories:
    button = InlineKeyboardButton(
        text=category[0],
        callback_data=str(category[1]))
    keyboard_category.insert(button)
else:
    button = InlineKeyboardButton(
        text='Другое',
        callback_data='1')
    keyboard_category.insert(button)
