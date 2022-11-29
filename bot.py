import datetime as dt
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
from aiogram.utils.exceptions import Unauthorized
from statistics import Statistics
from analitycs import Analitycs
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
# TODO отправлять одну и ту же статистику в гугл и в локальную

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nНапиши мне сообщение!')
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler(commands=['stat'])
async def process_stat_command(message: types.Message):
    await message.reply(Statistics.get_stat_message(), parse_mode="html")
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Напиши мне что-нибудь!\nЯ верну текст сообщения с временем его отправки!')
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler(commands=['statpic'])
async def process_statpic_command(message: types.Message):
    file_stat_image = Statistics.get_stat_image(message.from_user.id)
    photo = InputFile(file_stat_image)
    caption = 'Статистика по сообщениям от пользователей'
    await message.reply_photo(photo, caption=caption)
    Statistics.del_stat_image(file_stat_image)
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


@dp.message_handler()
async def echo(message: types.Message):
    Statistics.set_statistics(User(message.from_user.id, message.from_user.username))
    await message.answer(message.text + ' ' + get_current_time() + ' ' + get_current_date())
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name='message')


def bot_start():
    try:
        Statistics.load_stat()
        executor.start_polling(dp, skip_updates=True)
    except Unauthorized:
        logging.error('Invalid Token!')
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        sys.exit(1)
