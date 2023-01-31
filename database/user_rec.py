from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class UserRec(Base):
    __tablename__ = 'user'

    # id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String)
    statistics = relationship('StatisticsRec', cascade="all,delete", backref="statistics", lazy="joined")
    coffee = relationship('CoffeeRec', cascade="all,delete", backref="coffee", lazy="joined")

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return f"User(user_id={self.user_id!r}, user_name={self.user_name!r})"
