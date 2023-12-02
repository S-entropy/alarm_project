# 파이썬은 데이터베이스와 상호작용하는 객체를 통해 데이터베이스 사용. 직접 상호작용 X. sqlalchemy를 사용시 SQL문 쓰지 않고도 이용 가능.
import os
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

# 데이터베이스 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # __file__ : 현재 실행중인 파일
DB_NAME = 'users.db'

engine = create_engine(f"sqlite:///{BASE_DIR}/{DB_NAME}", echo=True)

session = scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )
)


@event.listens_for(Engine, identifier='connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()

# base.py
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

Model = declarative_base()
Model.query = session.query_property() # User.query 사용 가능


class TimeStampedModel(Model):
    __abstract__ = True # 직접 객체로 만들 수 없고 상속받아야 함.

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow()) # 마지막 update값만 남음에 유의. 변경이력 관리 불가

    # 한국 표준시
    # dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

#tables.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Time, DateTime
from sqlalchemy.orm import Relationship



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