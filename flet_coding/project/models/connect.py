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