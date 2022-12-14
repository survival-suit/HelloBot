import datetime as dt
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
from aiogram.utils.exceptions import Unauthorized
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from statistics import Statistics
from analitycs import Analitycs
from user import User
from coffee import Coffee


def get_token():
    try:
        token = os.environ['BOT_TOKEN']
        if token is None:
            raise KeyError('Token value is empty. Please set the value of environment variable BOT_TOKEN')
        return token
    except KeyError:
        logging.error('Please set the environment variable BOT_TOKEN')
        sys.exit(1)


def get_bot():
    try:
        bt = Bot(token=get_token())
    except Exception as ex:
        logging.error(ex)
    else:
        return bt


def get_bot_dispatcher(telegram_bot):
    try:
        dispatcher = Dispatcher(telegram_bot, storage=MemoryStorage())
    except Exception as ex:
        logging.error(ex)
    else:
        return dispatcher


def get_current_time():
    current_time = dt.datetime.now().strftime('%H:%M')
    return current_time


def get_current_date():
    current_date = dt.datetime.now().strftime('%d.%m.%Y')
    return current_date


bot = get_bot()
dp = Dispatcher(bot, storage=MemoryStorage())


def bot_start():
    try:
        Statistics.load_stat()
        executor.start_polling(dp, skip_updates=True)
    except Unauthorized:
        logging.error('Invalid Token!')
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        sys.exit(1)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nНапиши мне сообщение!')
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler(commands=['stat'])
async def process_stat_command(message: types.Message):
    await message.reply(Statistics.get_stat_message(), parse_mode="html")
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Напиши мне что-нибудь!\nЯ верну текст сообщения с временем его отправки!')
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


'''Присылаем картинкой статистику по количеству сообщений и команд пользователей'''


@dp.message_handler(commands=['statpic'])
async def process_statpic_command(message: types.Message):
    photo = InputFile(Statistics.get_stat_image())
    caption = 'Статистика по сообщениям от пользователей'
    await message.reply_photo(photo, caption=caption)
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


'''Команды и ф-ии работы с кофе'''


@dp.message_handler(commands=['coffee'])
async def start_coffee(message: types.Message):
    keyboard = Coffee.get_start_coffee_kb()
    await message.answer('Хочешь выпить кофе?', reply_markup=keyboard)
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.callback_query_handler(text="drink_coffee")
async def when_coffee(call: types.CallbackQuery):
    keyboard = Coffee.get_when_coffee_kb()
    await call.message.answer(f'Когда удобно?', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(Coffee.cd_when.filter(when_coffee=['coffee_today', 'coffee_tomorrow', 'coffee_weekend']))
async def send_req_coffee_owner(call: types.CallbackQuery, callback_data: dict):
    user_name = call.from_user.username
    user_name = '@' + user_name
    keyboard = Coffee.get_answer_coffee_kb()
    await bot.send_message(os.environ['OWNER_USER_ID'],
                           f'{user_name} хочет выпить кофе {Coffee.dict_when[callback_data["when_coffee"]]}! Выпить?',
                           reply_markup=keyboard)
    # await state.set_state(CoffeeStates.waiting_for_owner_answer.state)
    await call.answer(text="Вы согласились выпить кофе сегодня!", show_alert=True)


@dp.callback_query_handler(Coffee.cd_answer.filter(answer_coffee=['coffee_yes', 'coffee_no']))
async def answer_coffee_owner(call: types.CallbackQuery, callback_data: dict):
    # await state.update_data(owner_answer=Coffee.dict_answer[callback_data["answer_coffee"]])
    user_name = call.from_user.username
    user_name = '@' + user_name
    await call.answer(text=f'Вы ответили {user_name} {Coffee.dict_answer[callback_data["answer_coffee"]]}!',
                      show_alert=True)
    await bot.send_message(call.from_user.id,
                           f'На предложение выпить кофе ответили {Coffee.dict_answer[callback_data["answer_coffee"]]}.')


'''Отвечает пользователю его же сообщением только с датой и временем'''


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text + ' ' + get_current_time() + ' ' + get_current_date())
    user = User(message.from_user.id, message.from_user.username)
    Statistics.set_statistics(user, 'message')
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name='message')
