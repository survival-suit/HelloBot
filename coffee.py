from aiogram.utils.callback_data import CallbackData
from aiogram import types


class Coffee:
    cd = CallbackData('coffee', 'when_coffee')
    dict_when = {'coffee_today': 'сегодня', 'coffee_tomorrow': 'завтра', 'coffee_weekend': 'на выходных'}

    @staticmethod
    def get_start_coffee_kb():
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Выпить кофе', callback_data='drink_coffee'))
        return kb

    @staticmethod
    def get_when_coffee_kb():
        buttons = [
            types.InlineKeyboardButton(text='Сегодня', callback_data=Coffee.cd.new(when_coffee='coffee_today')),
            types.InlineKeyboardButton(text='Завтра', callback_data=Coffee.cd.new(when_coffee='coffee_tomorrow')),
            types.InlineKeyboardButton(text='На выходных', callback_data=Coffee.cd.new(when_coffee='coffee_weekend'))
        ]
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(*buttons)
        return kb
