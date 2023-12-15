"""Telegram Group Database Manager."""
from __future__ import annotations

import datetime
from typing import Dict, List, Optional, cast

import pytz
import sqlalchemy.exc
from cachetools import cached
from sqlalchemy import delete, desc, insert, select, text, update
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult, Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Delete, Select, distinct, or_
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.expression import func

from TEx.database import GROUPS_CACHE, USERS_CACHE
from TEx.database.db_manager import DbManager
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramMediaOrmEntity,
    TelegramMessageOrmEntity,
    TelegramUserOrmEntity,
)


class TelegramGroupDatabaseManager:
    """Telegram Group Database Manager."""

    @staticmethod
    def get_all_by_phone_number(phone_number: str) -> List[TelegramGroupOrmEntity]:
        """Retrieve all Groups using the Source Phone Number."""
        return cast(
            List[TelegramGroupOrmEntity],
            DbManager.SESSIONS['data'].execute(
                select(TelegramGroupOrmEntity)
                .where(TelegramGroupOrmEntity.source == phone_number),
                ).scalars().all(),
            )

    @staticmethod
    @cached(cache=GROUPS_CACHE)
    def get_by_id(pk: str) -> Optional[TelegramGroupOrmEntity]:
        """Retrieve one TelegramGroupOrmEntity by PK."""
        return cast(
            Optional[TelegramGroupOrmEntity],
            DbManager.SESSIONS['data'].get(TelegramGroupOrmEntity, pk),
            )

    @staticmethod
    def insert_or_update(entity_values: Dict) -> None:
        """Insert or Update one Telegram Group."""
        is_update: bool = True
        entity: Optional[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_by_id(entity_values['id'])
        if entity is None:
            entity = TelegramGroupOrmEntity(id=entity_values['id'])
            is_update = False

        cursor: CursorResult

        if is_update:
            cursor = DbManager.SESSIONS['data'].execute(
                update(TelegramGroupOrmEntity).
                where(TelegramGroupOrmEntity.id == entity_values['id']).
                values(entity_values),
                )
        else:
            cursor = DbManager.SESSIONS['data'].execute(
                insert(TelegramGroupOrmEntity).
                values(entity_values),
                )

        DbManager.SESSIONS['data'].commit()
        cursor.close()


class TelegramMessageDatabaseManager:
    """Telegram Message Database Manager."""

    @staticmethod
    def get_all_messages_from_group(group_id: int, order_by_desc: bool = False, message_datetime_limit_seconds: Optional[int] = None) -> List[TelegramMessageOrmEntity]:
        """Return all Messages from a Single Group."""
        select_statement: Select = select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == group_id)

        if message_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMessageOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=message_datetime_limit_seconds)),
                )

        if order_by_desc:
            select_statement = select_statement.order_by(desc('date_time'))

        return cast(
            List[TelegramMessageOrmEntity],
            DbManager.SESSIONS['data'].execute(select_statement).scalars().all(),
            )

    @staticmethod
    def insert(entity_values: Dict) -> None:
        """Insert or Update one Telegram Message."""
        try:
            cursor: CursorResult = DbManager.SESSIONS['data'].execute(
                insert(TelegramMessageOrmEntity).
                values(entity_values),
                )

            DbManager.SESSIONS['data'].commit()
            cursor.close()

        except sqlalchemy.exc.IntegrityError as exc:
            if 'UNIQUE' in exc.orig.args[0]:  # type: ignore
                return

            raise

    @staticmethod
    def get_max_id_from_group(group_id: int) -> Optional[int]:
        """Return the Maximum id from a Group (AKA: Last Offset)."""
        row: Optional[Row] = DbManager.SESSIONS['data'].execute(
            select(TelegramMessageOrmEntity)
            .where(TelegramMessageOrmEntity.group_id == group_id)
            .order_by(desc('id'))
            .limit(1),
            ).one_or_none()

        if row is None:
            return None

        return int(row[0].id)

    @staticmethod
    def count_messages_from_group(group_id: int, message_datetime_limit_seconds: Optional[int] = None) -> int:
        """Count all Messages from a Single Group."""
        select_statement: Select = select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == group_id)

        if message_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMessageOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=message_datetime_limit_seconds)),
                )

        select_statement = select_statement.with_only_columns(func.count())

        return cast(int, DbManager.SESSIONS['data'].execute(select_statement).scalar())

    @staticmethod
    def count_active_users_from_group(group_id: int, message_datetime_limit_seconds: Optional[int] = None) -> int:
        """Count all Active Users from a Single Group."""
        select_statement: Select = select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == group_id)

        if message_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMessageOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=message_datetime_limit_seconds)),
                )

        select_statement = select_statement.with_only_columns(func.count(distinct(TelegramMessageOrmEntity.from_id)))

        return cast(int, DbManager.SESSIONS['data'].execute(select_statement).scalar())

    @staticmethod
    def count_active_users(message_datetime_limit_seconds: Optional[int] = None) -> int:
        """Count all Users from a Single Group."""
        select_statement: Select = select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id > 0)

        if message_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMessageOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=message_datetime_limit_seconds)),
                )

        select_statement = select_statement.with_only_columns(func.count(distinct(TelegramMessageOrmEntity.from_id)))

        return cast(int, DbManager.SESSIONS['data'].execute(select_statement).scalar())

    @staticmethod
    def remove_all_messages_by_age(group_id: int, limit_days: int) -> int:
        """
        Remove all Messages older that Age in Seconds.

        :param group_id: Target Group ID
        :param limit_days: Age of Messages in Days
        :return: Number of Messages Removed
        """
        statement: Delete = delete(TelegramMessageOrmEntity)\
            .where(TelegramMessageOrmEntity.group_id == group_id)\
            .where(
                TelegramMessageOrmEntity.date_time <= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(days=limit_days)),
                )

        total_messages: int = cast(int, DbManager.SESSIONS['data'].execute(statement).rowcount)
        DbManager.SESSIONS['data'].commit()

        return total_messages


class TelegramUserDatabaseManager:
    """Telegram User Database Manager."""

    @staticmethod
    @cached(cache=USERS_CACHE)
    def get_by_id(pk: Optional[int]) -> Optional[TelegramUserOrmEntity]:
        """Retrieve one TelegramUserOrmEntity by PK."""
        if pk is None:
            return None

        return cast(
            Optional[TelegramUserOrmEntity],
            DbManager.SESSIONS['data'].get(TelegramUserOrmEntity, pk),
            )

    @staticmethod
    def insert_or_update(values: Dict) -> None:
        """Insert or Update one Telegram User."""
        TelegramUserDatabaseManager.__insert_or_update_single_entity(values)
        DbManager.SESSIONS['data'].commit()

    @staticmethod
    def insert_or_update_batch(values: Optional[List[Dict]]) -> None:
        """Insert or Update one Telegram User."""
        if values is None:
            return

        _ = [TelegramUserDatabaseManager.__insert_or_update_single_entity(item) for item in values]
        DbManager.SESSIONS['data'].commit()

    @staticmethod
    def __insert_or_update_single_entity(entity_values: Dict) -> None:
        """Insert or Update one Telegram User."""
        is_update: bool = True
        entity: Optional[TelegramUserOrmEntity] = TelegramUserDatabaseManager.get_by_id(entity_values['id'])
        if entity is None:
            entity = TelegramUserOrmEntity(id=entity_values['id'])
            is_update = False

        cursor: CursorResult

        if is_update:
            cursor = DbManager.SESSIONS['data'].execute(
                update(TelegramUserOrmEntity).
                where(TelegramUserOrmEntity.id == entity_values['id']).
                values(entity_values),
                )
        else:
            cursor = DbManager.SESSIONS['data'].execute(
                insert(TelegramUserOrmEntity).
                values(entity_values),
                )

        cursor.close()


class TelegramMediaDatabaseManager:
    """Telegram Media Database Manager."""

    @staticmethod
    def get_by_id(pk: Optional[int]) -> Optional[TelegramMediaOrmEntity]:
        """Retrieve one TelegramUserOrmEntity by PK."""
        if pk is None:
            return None

        return cast(
            Optional[TelegramMediaOrmEntity],
            DbManager.SESSIONS['data'].get(TelegramMediaOrmEntity, pk),
            )

    @staticmethod
    def insert(entity_values: Dict) -> int:
        """Insert or Update one Telegram User."""
        session: Session = DbManager.SESSIONS['data']

        cursor: CursorResult = session.execute(
            insert(TelegramMediaOrmEntity).
            values(entity_values),
            )
        session.commit()
        cursor.close()

        return int(cursor.inserted_primary_key[0])

    @staticmethod
    def get_all_medias_from_group_and_mimetype(group_id: int, mime_type: str, file_datetime_limit_seconds: Optional[int] = None, file_name_part: Optional[List[str]] = None) -> ChunkedIteratorResult:
        """
        Return all Messages from a Single Group.

        :param group_id: Target Group ID
        :param mime_type: Target Mime_Type
        :param file_datetime_limit_seconds: Age of File in Seconds
        :param file_name_part: Filter with Filename Part (Optional, use None for All Files)
        :return:
        """
        select_statement: Select = select(TelegramMediaOrmEntity)

        # File Age
        if file_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMediaOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=file_datetime_limit_seconds)),
                )

        # MimeType
        select_statement = select_statement.where(TelegramMediaOrmEntity.mime_type == mime_type)
        select_statement = select_statement.where(TelegramMediaOrmEntity.group_id == group_id)

        # Filename Filtering
        if file_name_part:
            parts_or_filter: List[BinaryExpression] = []

            for name_part in file_name_part:
                parts_or_filter.append(TelegramMediaOrmEntity.file_name.contains(name_part))  # type: ignore

            select_statement = select_statement.where(or_(*parts_or_filter))

        return DbManager.SESSIONS['data'].execute(select_statement)  # type: ignore

    @staticmethod
    def stats_all_medias_from_group_by_mimetype(group_id: int, file_datetime_limit_seconds: Optional[int] = None) -> Dict:
        """
        Generate Statistics of all Medias from a Single Group and Grouped by MimeType.

        :param group_id: Target Group ID
        :param file_datetime_limit_seconds: Age of File in Seconds
        :return: A List with Mime-Type, Number of Entries and Total Size in Bytes
        """
        select_statement: Select = select(TelegramMediaOrmEntity)

        # File Age
        if file_datetime_limit_seconds:
            select_statement = select_statement.where(
                TelegramMediaOrmEntity.date_time >= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(seconds=file_datetime_limit_seconds)),
                )

        # Group Clause
        select_statement = select_statement.where(TelegramMediaOrmEntity.group_id == group_id)
        select_statement = select_statement.with_only_columns(
            distinct(TelegramMediaOrmEntity.mime_type),
            func.count(TelegramMediaOrmEntity.mime_type),
            func.sum(TelegramMediaOrmEntity.size_bytes),
            )
        select_statement = select_statement.group_by(TelegramMediaOrmEntity.mime_type)
        select_statement = select_statement.group_by(TelegramMediaOrmEntity.group_id == group_id)

        medias: ChunkedIteratorResult = DbManager.SESSIONS['data'].execute(select_statement).all()

        h_result: Dict = {}

        # Group Results
        for media in medias:
            h_result[media[0]] = {'count': media[1], 'size_bytes': media[2]}

        return h_result

    @staticmethod
    def get_all_medias_by_age(group_id: int, media_limit_days: int) -> List[TelegramMediaOrmEntity]:
        """
        Remove all Medias older that Age in Seconds.

        :param group_id: Target Group ID
        :param media_limit_days: Age of Media in Days
        :return: Number of Medias Removed
        """
        statement: Delete = select(TelegramMediaOrmEntity).where(  # type: ignore
            TelegramMediaOrmEntity.date_time <= (datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(days=media_limit_days)),
            )

        statement = statement.where(TelegramMediaOrmEntity.group_id == group_id)

        return cast(
            List[TelegramMediaOrmEntity],
            DbManager.SESSIONS['data'].execute(statement).scalars().all(),
            )

    @staticmethod
    def delete_media_by_id(media_id: int) -> None:
        """
        Remove Media by PK.

        :param group_id: Target Group ID
        :param media_id: Media ID
        :return:
        """
        statement: Delete = delete(TelegramMediaOrmEntity).where(TelegramMediaOrmEntity.id == media_id)
        DbManager.SESSIONS['data'].execute(statement)
        DbManager.SESSIONS['data'].commit()

    @staticmethod
    def apply_db_maintenance() -> None:
        """
        Remove all Medias older that Age in Seconds.

        :param group_id: Target Group ID
        :param file_datetime_limit_seconds: Age of File in Seconds
        :return: Number of Medias Removed
        """
        DbManager.SESSIONS['data'].execute(text('vacuum'))
