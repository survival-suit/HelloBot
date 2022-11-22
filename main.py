import logging
import bot as b
from logger import set_logging

if __name__ == '__main__':
    try:
        set_logging(logging.ERROR)
        b.bot_start()
    except Exception as ex:
        logging.error(ex)
