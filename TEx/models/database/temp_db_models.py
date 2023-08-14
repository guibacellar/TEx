"""Temporary Data Model."""

from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TempDataBaseDeclarativeBase(DeclarativeBase):  # type: ignore
    """Global Temporary Declarative Base."""


class TempDataOrmEntity(TempDataBaseDeclarativeBase):
    """Temporary Data ORM Model."""

    __bind_key__ = 'temp'
    __tablename__ = 'temporary_data'

    path: Mapped[str] = mapped_column(String(255), primary_key=True)
    module: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    data: Mapped[str] = mapped_column(String)
    created_at: Mapped[Integer] = mapped_column(Integer)
    valid_at: Mapped[Integer] = mapped_column(Integer)


class StateFileOrmEntity(TempDataBaseDeclarativeBase):
    """Temporary Data ORM Model."""

    __bind_key__ = 'temp'
    __tablename__ = 'state_file'

    path: Mapped[str] = mapped_column(String(255), primary_key=True)
    data: Mapped[str] = mapped_column(String)
    created_at: Mapped[Integer] = mapped_column(Integer)
