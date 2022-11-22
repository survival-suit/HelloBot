import logging
import json
import os

from user import User


class Statistics:
    file_name = 'statistics.json'
    statistics_list = []

    """Загрузка статистики из файла"""

    @staticmethod
    def load_stat():
        if os.path.isfile(Statistics.file_name) and os.stat(Statistics.file_name).st_size != 0:
            try:
                f = open(Statistics.file_name, 'r')
                users = json.load(f)
                for user in users:
                    Statistics.statistics_list.append(User(user['user_id'], user['user_req']))
            except Exception as ex:
                logging.error(ex)

    @staticmethod
    def print_statistics_list():
        for stat in Statistics.statistics_list:
            print(f'{stat}')

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
