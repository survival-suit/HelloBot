from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


class Base:
    pass


Base = declarative_base(cls=Base)

# engine = create_engine('sqlite:///C:\\sqlitedbs\\school.db', echo=True)
# Base.metadata.create_all(engine)

from .statistics_rec import StatisticsRec
from .user_rec import UserRec