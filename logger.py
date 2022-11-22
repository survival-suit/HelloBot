import logging
import sys


def set_logging(level):
    logging.basicConfig(level=level,
                        format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[
                            logging.FileHandler('hellobot.log'),
                            logging.StreamHandler(sys.stdout)
                        ])
