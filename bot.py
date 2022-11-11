import logging
import datetime as dt
import os
import sys

import aiogram
from aiogram import Bot, Dispatcher, executor, types


def set_logging(level):
    logging.basicConfig(level=level,
                        format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[
                            logging.FileHandler('hellobot.log'),
                            logging.StreamHandler(sys.stdout)
                        ])


set_logging(logging.ERROR)


def get_token():
    try:
       os.environ['BOT_TOKEN']
    except KeyError:
       logging.error('Please set the environment variable BOT_TOKEN')
       sys.exit(1)
    except ValueError:
       logging.error('Please set the value of environment variable BOT_TOKEN')
       sys.exit(1)
    else:
        return os.environ['BOT_TOKEN']


def get_bot_dispatcher():
    try:
        bot = Bot(token=get_token())
    except aiogram.utils.exceptions.ValidationError:
        logging.error('Telegram token (variable BOT_TOKEN) is invalid!')
        sys.exit(1)
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
    await message.reply("Привет!\nНапиши мне сообщение!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь!\nЯ верну текст сообщения с временем его отправки!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text + ' ' + get_current_time() + ' ' + get_current_date())


def bot_start():
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        sys.exit(1)

