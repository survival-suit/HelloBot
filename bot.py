import datetime as dt
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Unauthorized
from statistics import Statistics
from user import User


def get_token():
    try:
        token = os.environ['BOT_TOKEN']
        if token is None:
            raise KeyError('Token value is empty. Please set the value of environment variable BOT_TOKEN')
        return token
    except KeyError:
        logging.error('Please set the environment variable BOT_TOKEN')
        sys.exit(1)


def get_bot_dispatcher():
    try:
        bot = Bot(token=get_token())
    except Exception as ex:
        logging.error(ex)
    else:
        return Dispatcher(bot)


def get_current_time():
    current_time = dt.datetime.now().strftime('%H:%M')
    return current_time


def get_current_date():
    current_date = dt.datetime.now().strftime('%d.%m.%Y')
    return current_date


dp = get_bot_dispatcher()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nНапиши мне сообщение!')


@dp.message_handler(commands=['stat'])
async def process_stat_command(message: types.Message):
    for user in Statistics.statistics_list:
        await message.reply(f'Пользователь: {user.user_id} Кол-во запросов: {user.user_req}')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Напиши мне что-нибудь!\nЯ верну текст сообщения с временем его отправки!')


@dp.message_handler()
async def echo(message: types.Message):
    Statistics.set_statistics(User(message.from_user.id))
    await message.answer(message.text + ' ' + get_current_time() + ' ' + get_current_date())


def bot_start():
    try:
        Statistics.get_stat()
        executor.start_polling(dp, skip_updates=True)
    except Unauthorized:
        logging.error('Invalid Token!')
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        sys.exit(1)
