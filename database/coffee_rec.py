from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from . import Base


class CoffeeRec(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, nullable=False)
    date_time = Column(DateTime)
    coffee_day = Column(Date)
    user_from_id = Column(Integer, ForeignKey('user.user_id'))
    status = Column(Integer)

    def __init__(self, date_time, coffee_day, user_from_id, status):
        self.date_time = date_time
        self.coffee_day = coffee_day
        self.user_from_id = user_from_id
        self.status = status

    def __repr__(self):
        return f"User(id={self.id!r}, date_time={self.date_time!r}, " \
               f"coffee_day={self.coffee_day!r}, user_from_id={self.user_from_id!r}, " \
               f"status={self.status!r} )"
