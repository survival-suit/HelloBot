import datetime as dt
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
from aiogram.utils.exceptions import Unauthorized
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters
from statistics import Statistics
from analitycs import Analitycs
from user import User
from coffee import Coffee
from database.dbservice import DBService


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


def set_statistics(message):
    user = User(message.from_user.id, message.from_user.username)
    DBService.set_statistics(user, message.get_command().replace('/', ''))
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name=message.get_command().replace('/', ''))


bot = get_bot()
dp = Dispatcher(bot, storage=MemoryStorage())


def bot_start():
    try:
        DBService.init_db()
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
    set_statistics(message)


@dp.message_handler(commands=['stat'])
async def process_stat_command(message: types.Message):
    await message.reply(DBService.get_stat_message(), parse_mode="html")
    set_statistics(message)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply('Напиши мне что-нибудь!\nЯ верну текст сообщения с временем его отправки!')
    set_statistics(message)


'''Присылаем картинкой статистику по количеству сообщений и команд пользователей'''


@dp.message_handler(commands=['statpic'])
async def process_statpic_command(message: types.Message):
    photo = InputFile(DBService.get_stat_image())
    caption = 'Статистика по сообщениям от пользователей'
    await message.reply_photo(photo, caption=caption)
    set_statistics(message)


'''Команды и ф-ии работы с кофе'''


@dp.message_handler(commands=['coffee'])
async def start_coffee(message: types.Message):
    keyboard = Coffee.get_start_coffee_kb()
    await message.answer('Хочешь выпить кофе?', reply_markup=keyboard)
    set_statistics(message)


@dp.message_handler(commands=['coffee_today'])
async def coffee_today(message: types.Message):
    user_id = message.from_user.id
    result = DBService.check_coffee_today(user_id)
    if result is None:
        await message.reply('На сегодня у вас не запланирован кофе.')
    else:
        pretty_coffee_day = result.coffee_day.strftime("%d.%m.%Y")
        info_message = f'На сегодня {pretty_coffee_day} у вас запланирован кофе'
        if user_id == int(os.environ['OWNER_USER_ID']):
            user_name = '@' + DBService.get_user_by_id(result.user_from_id)
            await message.reply(info_message + f' c {user_name}')
        else:
            await message.reply(info_message + '.')
    set_statistics(message)


@dp.callback_query_handler(text="drink_coffee")
async def when_coffee(call: types.CallbackQuery):
    keyboard = Coffee.get_when_coffee_kb()
    await call.message.answer(f'Когда удобно?', reply_markup=keyboard)


@dp.callback_query_handler(Coffee.cd_when.filter(when_coffee=['coffee_today', 'coffee_tomorrow', 'coffee_weekend']))
async def send_req_coffee_owner(call: types.CallbackQuery, callback_data: dict):
    user = User(call.from_user.id, call.from_user.username)
    coffee_rec = DBService.set_coffee(user, callback_data["when_coffee"])
    pretty_coffee_day = coffee_rec.coffee_day.strftime("%d.%m.%Y")
    if coffee_rec.status == -1:
        await call.answer(text=f'К сожалению, {Coffee.dict_when[callback_data["when_coffee"]]} {pretty_coffee_day} выпить кофе'
                               f' не получится, график переполнен. Попробуйте выбрать другой день: /coffee',
                          show_alert=True)
    else:
        message = f'Вы согласились выпить кофе {Coffee.dict_when[callback_data["when_coffee"]]} {pretty_coffee_day}!Ждите ответа.'
        await call.answer(text=message, show_alert=True)
        await bot.send_message(call.from_user.id, 'Напоминаение: '+message)
        # sending message to bot for admin
        message = f"Новый запрос на кофе от @{call.from_user.username}"
        message += f"\n\n/coffee_accept_{coffee_rec.id}"
        await bot.send_message(os.environ['OWNER_USER_ID'], message)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['coffee_accept_([0-9]*)']))
async def coffee_accept(message: types.Message):
    row_id = message.text.replace("/coffee_accept_", "")
    coffee_rec = DBService.get_offer_to_coffee(row_id)
    user_name = '@' + DBService.get_user_by_id(coffee_rec.user_from_id)
    buttons = [
        types.InlineKeyboardButton(text='Да', callback_data='coffee_y_' + row_id),
        types.InlineKeyboardButton(text='Нет', callback_data='coffee_n_' + row_id)
    ]
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)

    await message.answer(f'Пользователь {user_name} хочет выпить c вами кофе {coffee_rec.coffee_day.strftime("%d.%m.%Y")}. '
                         f'Этот день в графике свободен. Выпить кофе с пользователем?', reply_markup=kb)


@dp.callback_query_handler(filters.Regexp(regexp='coffee_[yn]_([0-9]*)'))
async def answer_coffee_owner(call: types.CallbackQuery):
    message_text = call.data
    row_id = message_text[9:]
    answer = message_text.replace(row_id, "")
    status = 1
    answer_text = 'да'
    if answer == 'coffee_n_':
        status = -2
        answer_text = 'нет'

    coffee_rec = DBService.get_offer_to_coffee(row_id)
    user_name = '@' + DBService.get_user_by_id(coffee_rec.user_from_id)
    pretty_coffee_day = coffee_rec.coffee_day.strftime("%d.%m.%Y")
    DBService.update_status(row_id, status)
    admin_message = f'Вы ответили {answer_text} на предложение {user_name} выпить кофе в дату {pretty_coffee_day}!'
    user_message = f'На предложение выпить кофе в дату {pretty_coffee_day} ответили: {answer_text}.'

    await call.answer(text=admin_message, show_alert=True)
    await bot.send_message(os.environ['OWNER_USER_ID'], admin_message)
    await bot.send_message(coffee_rec.user_from_id, user_message)


'''Отвечает пользователю его же сообщением только с датой и временем'''


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text + ' ' + get_current_time() + ' ' + get_current_date())

    user = User(message.from_user.id, message.from_user.username)
    DBService.set_statistics(user, 'message')
    Analitycs.send_analytics(user_id=message.from_user.id, lang_code=message.from_user.language_code,
                             action_name='message')
