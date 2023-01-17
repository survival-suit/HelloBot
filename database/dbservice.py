import logging
import os
import random
import database
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from aiogram.utils.markdown import hlink
from sqlalchemy.orm import Session, lazyload
from sqlalchemy import create_engine, select
from analitycs import Analitycs
from database import StatisticsRec, UserRec
from user import User
from io import BytesIO


class DBService:
    db_url = os.environ['DB_URL']
    engine = create_engine(db_url, echo=True)

    @staticmethod
    def init_db():
        database.Base.metadata.create_all(DBService.engine)

    """Загрузка статистики из базы в список User"""

    @staticmethod
    def get_statistics():
        with Session(DBService.engine) as session:
            # statistics_dict = {}
            statistics_list = []
            load_stat_query = session.query(UserRec).options(lazyload(UserRec.statistics)).all()
            for query in load_stat_query:
                user = User(query.user_id, query.user_name, DBService.get_command_dict(query.statistics))
                statistics_list.append(user)
                # statistics_dict[query.user_id] = {'user_name': f'{query.user_name}', 'commands': DBService.get_command_dict(query.statistics)}
        return statistics_list

    """Получение словаря команд из списка команд"""

    @staticmethod
    def get_command_dict(list_command):
        command_dict = {}
        for stat in list_command:
            if not command_dict:
                command_dict[stat.command] = 1
            else:
                if stat.command in command_dict:
                    command_dict[stat.command] += 1
                else:
                    command_dict[stat.command] = 1
        return command_dict

    @staticmethod
    def get_stat_message():
        text_link = hlink("Google Analitycs", Analitycs.SHARE_URL)
        message_text = ''
        for user in DBService.get_statistics():
            message_text += f'Пользователь: {user.user_id} Имя: {user.user_name} Общее кол-во запросов: {user.get_action_value("all")} \n'
        message_text += f'\n\nПдробнее в {text_link}'
        return message_text

    '''Генерация и получение изображения статистики пользователей по кол-ву сообщений'''

    @staticmethod
    def get_stat_image():
        all_colors = [k for k, v in mcolors.cnames.items()]
        all_colors.remove('black')
        all_colors.remove('white')
        user_name_list = []
        user_req_list = []
        random_color_list = []
        random_color = random.choice(all_colors)
        for user in DBService.get_statistics():
            user_name_list.append(user.__dict__['user_name'])
            user_req_list.append(user.get_action_value('all'))
            if not random_color_list:
                random_color_list.append(random_color)
            else:
                while random_color_list[-1] == random_color:
                    random_color = random.choice(all_colors)
                random_color_list.append(random_color)
        fig, ax = plt.subplots()
        fig.set_facecolor('floralwhite')
        ax.bar(user_name_list, user_req_list, color=random_color_list, edgecolor='darkgrey')
        ax.set_ylabel('Количество сообщений')
        ax.set_title('Статистика по сообщениям от пользователей')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        return buf
        buf.close()

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
