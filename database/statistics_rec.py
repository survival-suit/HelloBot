from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from . import Base


class StatisticsRec(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, nullable=False)
    time = Column(DateTime)
    command = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __init__(self, time, command, user_id):
        self.time = time
        self.command = command
        self.user_id = user_id

    def __repr__(self):
        return f"User(id={self.id!r}, time={self.time!r}, command={self.command!r}, user_id={self.user_id!r})"
