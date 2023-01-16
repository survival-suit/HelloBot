import logging
import random
import os
import database
import datetime

from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, func
from database import StatisticsRec, UserRec
from analitycs import Analitycs
from aiogram.utils.markdown import hlink

from user import User


class DBService:
    db_url = os.environ['DB_URL']
    engine = create_engine(db_url, echo=True)

    @staticmethod
    def init_db():
        database.Base.metadata.create_all(DBService.engine)

    """Загрузка статистики из файла"""

    @staticmethod
    def get_statistics():
        statistics_list = []
        with Session(DBService.engine) as session:
            statement = select(
                StatisticsRec.command,
                StatisticsRec.user_id,
                UserRec.user_name,
                func.count(StatisticsRec.command).label('total'))\
                .join(UserRec, UserRec.user_id == StatisticsRec.user_id)\
                .group_by(StatisticsRec.user_id, StatisticsRec.command)
            load_stat_query = session.execute(statement).all()

        for query in load_stat_query:
            if not statistics_list:
                user = User(query[1], query[2])
                user.action_add(query[0], query[3])
                statistics_list.append(user)
            else:
                for stat in statistics_list:
                    if stat.user_id == query[1]:
                        stat.user_req[query[0]] = query[3]
                    else:
                        user = User(query[1], query[2])
                        user.action_add(query[0], query[3])
                        statistics_list.append(user)
        return statistics_list


    """Формирование статистики для сообщения пользователю"""

    @staticmethod
    def get_stat_message():
        text_link = hlink("Google Analitycs", Analitycs.SHARE_URL)
        message_text = ''
        for user in DBService.get_statistics():
            message_text += f'Пользователь: {user.user_id} Имя: {user.user_name} Общее кол-во запросов: {user.get_action_value("all")} \n'
        message_text += f'\n\nПдробнее в {text_link}'
        return message_text

    '''Добавление или апдейт статистики(в базе и статической переменной)'''

    @staticmethod
    def set_statistics(user_object, action_name):
        with Session(DBService.engine) as session:
            try:
                statement = select(UserRec).filter_by(user_id=user_object.user_id)
                result = session.execute(statement).scalars().first()
                if result is None:
                    user_rec = UserRec(user_id=user_object.user_id, user_name=user_object.user_name)
                    session.add(user_rec)
                    session.commit()

                statistics_rec = StatisticsRec(time=datetime.datetime.now(), command=action_name,
                                               user_id=user_object.user_id)
                session.add(statistics_rec)
                session.commit()
            except Exception as ex:
                logging.error(ex)
