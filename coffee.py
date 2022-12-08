from aiogram.utils.callback_data import CallbackData
from aiogram import types


class Coffee:
    cd_when = CallbackData('cd_when_coffee', 'when_coffee')
    cd_answer = CallbackData('cd_answer_coffee', 'answer_coffee')

    dict_when = {'coffee_today': 'сегодня', 'coffee_tomorrow': 'завтра', 'coffee_weekend': 'на выходных'}
    dict_answer = {'coffee_yes': 'да', 'coffee_no': 'нет'}

    @staticmethod
    def get_start_coffee_kb():
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Выпить кофе', callback_data='drink_coffee'))
        return kb

    @staticmethod
    def get_when_coffee_kb():
        buttons = [
            types.InlineKeyboardButton(text='Сегодня', callback_data=Coffee.cd_when.new(when_coffee='coffee_today')),
            types.InlineKeyboardButton(text='Завтра', callback_data=Coffee.cd_when.new(when_coffee='coffee_tomorrow')),
            types.InlineKeyboardButton(text='На выходных',
                                       callback_data=Coffee.cd_when.new(when_coffee='coffee_weekend'))
        ]
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(*buttons)
        return kb

    @staticmethod
    def get_answer_coffee_kb():
        buttons = [
            types.InlineKeyboardButton(text='Да', callback_data=Coffee.cd_answer.new(answer_coffee='coffee_yes')),
            types.InlineKeyboardButton(text='Нет', callback_data=Coffee.cd_answer.new(answer_coffee='coffee_no'))
        ]
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(*buttons)
        return kb
