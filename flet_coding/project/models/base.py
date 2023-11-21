from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base

from flet_coding.project.models.connect import session

Model = declarative_base()
Model.query = session.query_property() # User.query 사용 가능


class TimeStampedModel(Model):
    __abstract__ = True # 직접 객체로 만들 수 없고 상속받아야 함.

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow()) # 마지막 update값만 남음에 유의. 변경이력 관리 불가

    # 한국 표준시
    # dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
