from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time, DateTime
from sqlalchemy.orm import Relationship

from flet_coding.project.models.base import TimeStampedModel


class User(TimeStampedModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    email_key = Column(String(1000), nullable=False)
    password = Column(String(320), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    alarms = Relationship('Alarm', back_populates='user')

class Alarm(TimeStampedModel):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    data = Column(String(1000), nullable=False)
    repeat_now = Column(Boolean, nullable=False)
    repeat_week = Column(Integer, nullable=False)
    alarm_date = Column(Date, nullable=False)
    alarm_time = Column(Time, nullable=False)

    user = Relationship('User', back_populates='alarms')
    alarm_repeat = Relationship('Alarm_repeat', back_populates='alarm')

class Alarm_repeat(TimeStampedModel):
    __tablename__ = 'alarm_repeats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alarm_id = Column(Integer, ForeignKey('alarms.id', ondelete='CASCADE'))
    repeat_interval = Column(Integer, nullable=False)
    repeat_time = Column(DateTime, nullable=False)

    alarm = Relationship('Alarm', back_populates='alarm_repeat')