"""Projects DB Models."""
from __future__ import annotations

import datetime
import logging
from typing import Optional

import sqlalchemy
from sqlalchemy import Boolean, DateTime, Index, Integer, MetaData, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from TEx.database.db_manager import DbManager

logger = logging.getLogger('TelegramExplorer')


class TelegramDataBaseDeclarativeBase(DeclarativeBase):
    """Global Telegram DB Declarative Base."""

    @staticmethod
    def apply_migrations() -> None:
        """Apply all Migrations."""
        meta: MetaData = sqlalchemy.MetaData()
        meta.reflect(bind=DbManager.SQLALCHEMY_BINDS['data'])

        # ix_telegram_message_group_id_date - V0.3.0
        TelegramDataBaseDeclarativeBase.__create_index(
            metadata=meta,
            table_name='telegram_message',
            index_name='ix_telegram_message_group_id_date',
            version='V0.3.0',
            field_spec=(TelegramMessageOrmEntity.group_id, TelegramMessageOrmEntity.date_time.desc())
        )

        # ix_telegram_media_group_id_date - V0.3.0
        TelegramDataBaseDeclarativeBase.__create_index(
            metadata=meta,
            table_name='telegram_media',
            index_name='ix_telegram_media_group_id_date',
            version='V0.3.0',
            field_spec=(TelegramMediaOrmEntity.group_id, TelegramMediaOrmEntity.date_time.desc())
        )

    @staticmethod
    def __create_index(metadata: MetaData, table_name: str, index_name: str, version: str, field_spec: tuple) -> None:

        # Messages Table
        table: Table = metadata.tables[table_name]

        # ix_telegram_message_group_id_date - V0.3.0
        index_exists: bool = TelegramDataBaseDeclarativeBase.__check_index_exists(
            table=table,
            index_name=index_name
        )

        if not index_exists:
            logger.info(f'\t[*] APPLYING DB MIGRATION ({version}) - {index_name}')

            new_index: Index = sqlalchemy.Index(
                index_name,
                *field_spec
            )
            new_index.create(bind=DbManager.SQLALCHEMY_BINDS['data'])

    @staticmethod
    def __check_index_exists(table: Table, index_name: str) -> bool:
        """Check if Index Exists on Table."""
        return len([item for item in table.indexes if item.name == index_name]) == 1


class TelegramGroupOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Group ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    constructor_id: Mapped[str] = mapped_column(String(255))
    access_hash: Mapped[str] = mapped_column(String(255))
    group_username: Mapped[str] = mapped_column(String(1024), index=True)
    title: Mapped[str] = mapped_column(String(4098), index=True)

    fake: Mapped[bool] = mapped_column(Boolean)
    gigagroup: Mapped[bool] = mapped_column(Boolean)
    has_geo: Mapped[bool] = mapped_column(Boolean)
    restricted: Mapped[bool] = mapped_column(Boolean)
    scam: Mapped[bool] = mapped_column(Boolean)
    verified: Mapped[bool] = mapped_column(Boolean)

    participants_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    photo_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_base64: Mapped[Optional[str]] = mapped_column(String(1024000), nullable=True)
    photo_name: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    source: Mapped[str] = mapped_column(String(255), index=True)


class TelegramMessageOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Message ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    media_id: Mapped[Optional[int]] = mapped_column(Integer, index=True)

    date_time: Mapped[datetime.datetime] = mapped_column(DateTime)
    message: Mapped[str] = mapped_column(String(65535))
    raw: Mapped[str] = mapped_column(String(65535))

    from_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    from_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    to_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_reply: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    reply_to_msg_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class TelegramMediaOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Media ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_media'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(Integer, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, index=True)
    file_name: Mapped[str] = mapped_column(String(1024))

    extension: Mapped[str] = mapped_column(String(16))
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    date_time: Mapped[datetime.datetime] = mapped_column(DateTime)

    mime_type: Mapped[str] = mapped_column(String(128))
    size_bytes: Mapped[int] = mapped_column(Integer)

    title: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)


class TelegramUserOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram User ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    is_bot: Mapped[bool] = mapped_column(Boolean)
    is_fake: Mapped[bool] = mapped_column(Boolean)
    is_self: Mapped[bool] = mapped_column(Boolean)
    is_scam: Mapped[bool] = mapped_column(Boolean)
    is_verified: Mapped[bool] = mapped_column(Boolean)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(1024), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    photo_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    photo_base64: Mapped[Optional[str]] = mapped_column(String(1024000), nullable=True)
    photo_name: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
