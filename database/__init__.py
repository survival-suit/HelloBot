from sqlalchemy.ext.declarative import declarative_base


class Base:
    pass


Base = declarative_base(cls=Base)

from .statistics_rec import StatisticsRec
from .user_rec import UserRec
from .coffee_rec import CoffeeRec
