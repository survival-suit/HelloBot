import logging
import random
import json
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from user import User
from analitycs import Analitycs
from aiogram.utils.markdown import hlink


class Statistics:
    file_name = 'statistics.json'
    stat_image_ext = '.png'
    statistics_list = []

    """Загрузка статистики из файла"""
    @staticmethod
    def load_stat():
        if os.path.isfile(Statistics.file_name) and os.stat(Statistics.file_name).st_size != 0:
            try:
                f = open(Statistics.file_name, 'r')
                users = json.load(f)
                for user in users:
                    Statistics.statistics_list.append(User(user['user_id'], user['user_name'], user['user_req']))
            except Exception as ex:
                logging.error(ex)

    """Формирование статистики для сообщения пользователю"""
    @staticmethod
    def get_stat_message():
        text_link = hlink("Google Analitycs", Analitycs.SHARE_URL)
        message_text = ''
        for user in Statistics.statistics_list:
            message_text += f'Пользователь: {user.user_id} Имя: {user.user_name} Кол-во запросов: {user.user_req} \n'
        message_text += f'\n\nПдробнее в {text_link}'
        return message_text

    '''Генерация и получение изображения статистики пользователей по кол-ву сообщений'''
    @staticmethod
    def get_stat_image(user_id): # TODO использовать генерацию памяти
        all_colors = [k for k, v in mcolors.cnames.items()]
        all_colors.remove('black')
        all_colors.remove('white')
        file_stat_image = str(user_id) + Statistics.stat_image_ext
        user_name_list = []
        user_req_list = []
        random_color_list = []
        random_color = random.choice(all_colors)
        for user in Statistics.statistics_list:
            user_name_list.append(user.__dict__['user_name'])
            user_req_list.append(user.__dict__['user_req'])
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
        #ax.set_xticks(user_name_list)
        #ax.set_xticklabels(user_req_list)
        plt.savefig(file_stat_image)
        plt.close(fig)
        return file_stat_image

    '''Удаление изображения со статистикой'''
    @staticmethod
    def del_stat_image(file_stat_image):
        os.remove(file_stat_image)

    '''Добавление или апдейт статистики(в файле и статической переменной)'''
    @staticmethod
    def set_statistics(user_object):
        if os.path.isfile(Statistics.file_name):
            try:
                list_dict = []
                f = open(Statistics.file_name, 'w')
                if not Statistics.statistics_list:
                    Statistics.statistics_list.append(user_object)
                    list_dict.append(user_object.__dict__)
                else:
                    for user in Statistics.statistics_list:
                        if user_object.user_id == user.user_id:
                            user.user_req += 1
                            break
                    else:
                        Statistics.statistics_list.append(user_object)
                    for user in Statistics.statistics_list:
                        list_dict.append(user.__dict__)
                json.dump(list_dict, f)
                f.close()
            except Exception as ex:
                logging.error(ex)
