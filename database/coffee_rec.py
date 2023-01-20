from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from . import Base


class CoffeeRec(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, nullable=False)
    time = Column(DateTime)
    coffee_day = Column(Date)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __init__(self, time, coffee_day, user_id):
        self.time = time
        self.coffee_day = coffee_day
        self.user_id = user_id

    def __repr__(self):
        return f"User(id={self.id!r}, time={self.time!r}, coffee_day={self.coffee_day!r}, user_id={self.user_id!r})"
