"""Projects DB Models."""

import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

TelegramDataBaseDeclarativeBase = declarative_base()
TelegramMediaDataBaseDeclarativeBase = declarative_base()


class TelegramGroupOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Group ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_group'

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    constructor_id: str = Column(String(255))
    access_hash: str = Column(String(255))
    group_username: str = Column(String(1024), index=True)
    title: str = Column(String(4098), index=True)

    fake: bool = Column(Boolean)
    gigagroup: bool = Column(Boolean)
    has_geo: bool = Column(Boolean)
    restricted: bool = Column(Boolean)
    scam: bool = Column(Boolean)
    verified: bool = Column(Boolean)

    participants_count: int = Column(Integer)

    photo_id: int = Column(Integer)
    photo_base64: str = Column(String(1024000))
    photo_name: str = Column(String(1024))

    source: str = Column(String(255), index=True)


class TelegramMessageOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram Message ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_message'

    id: int = Column(Integer, primary_key=True)  # noqa: A003
    group_id: int = Column(Integer, primary_key=True, index=True)
    media_id: Optional[int] = Column(Integer, index=True)

    date_time: datetime.datetime = Column(DateTime)
    message: str = Column(String(65535))
    raw: str = Column(String(65535))

    from_id: int = Column(Integer)
    from_type: str = Column(String(10))
    to_id: int = Column(Integer)

    is_reply: bool = Column(Boolean)
    reply_to_msg_id: int = Column(Integer)


class TelegramMediaOrmEntity(TelegramMediaDataBaseDeclarativeBase):
    """Telegram Media ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_media'

    id: int = Column(Integer, primary_key=True, autoincrement=True)  # noqa: A003
    telegram_id: int = Column(Integer)
    file_name: str = Column(String(1024))

    extension: str = Column(String(16))
    height: int = Column(Integer)
    width: int = Column(Integer)

    date_time: datetime.datetime = Column(DateTime)

    mime_type: str = Column(String(128))
    size_bytes: int = Column(Integer)

    title: str = Column(String(1024))
    name: str = Column(String(1024))

    b64_content: str = Column(String(256000000))  # 256 MB


class TelegramUserOrmEntity(TelegramDataBaseDeclarativeBase):
    """Telegram User ORM Model."""

    __bind_key__ = 'data'
    __tablename__ = 'telegram_user'

    id: int = Column(Integer, primary_key=True)  # noqa: A003

    is_bot: bool = Column(Boolean)
    is_fake: bool = Column(Boolean)
    is_self: bool = Column(Boolean)
    is_scam: bool = Column(Boolean)
    is_verified: bool = Column(Boolean)
    first_name: str = Column(String(255))
    last_name: str = Column(String(255))
    username: str = Column(String(1024))
    phone_number: str = Column(String(255))

    photo_id: int = Column(Integer)
    photo_base64: str = Column(String(1024000))
    photo_name: str = Column(String(1024))
