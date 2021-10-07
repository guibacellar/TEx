"""Temporary Data Model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

TempDataBaseDeclarativeBase = declarative_base()


class TempDataOrmEntity(TempDataBaseDeclarativeBase):
    """Temporary Data ORM Model."""

    __bind_key__ = 'temp'
    __tablename__ = 'temporary_data'

    path = Column(String(255), primary_key=True)
    module = Column(String(255))
    data = Column(String)
    created_at = Column(Integer)
    valid_at = Column(Integer)


class StateFileOrmEntity(TempDataBaseDeclarativeBase):
    """Temporary Data ORM Model."""

    __bind_key__ = 'temp'
    __tablename__ = 'state_file'

    path = Column(String(255), primary_key=True)
    data = Column(String)
    created_at = Column(Integer)
