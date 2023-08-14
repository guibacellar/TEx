"""Projects DB Models."""

import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class TelegramDataBaseDeclarativeBase(DeclarativeBase):  # type: ignore
    """Global Telegram DB Declarative Base."""


class TelegramGroupOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Group ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_group'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # noqa: A003
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003

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
