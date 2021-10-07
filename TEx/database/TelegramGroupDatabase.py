"""Telegram Group Database Manager."""
from typing import Dict, List, Optional, cast

from sqlalchemy import desc, insert, select, update
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.sql import Select

from TEx.database import data_session
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
            data_session.execute(
                select(TelegramGroupOrmEntity)
                .where(TelegramGroupOrmEntity.source == phone_number)
                ).scalars().all()
            )

    @staticmethod
    def get_by_id(pk: str) -> Optional[TelegramGroupOrmEntity]:
        """Retrieve one TelegramGroupOrmEntity by PK."""
        return cast(
            Optional[TelegramGroupOrmEntity],
            data_session.get(TelegramGroupOrmEntity, pk)
            )

    @staticmethod
    def insert_or_update(entity_values: Dict) -> None:
        """Insert or Update one Telegram Group."""
        is_update: bool = True
        entity: Optional[TelegramGroupOrmEntity] = TelegramGroupDatabaseManager.get_by_id(entity_values['id'])
        if entity is None:
            entity = TelegramGroupOrmEntity(id=entity_values['id'])
            is_update = False

        if is_update:
            data_session.execute(
                update(TelegramGroupOrmEntity).
                where(TelegramGroupOrmEntity.id == entity_values['id']).
                values(entity_values)
                )
        else:
            data_session.execute(
                insert(TelegramGroupOrmEntity).
                values(entity_values)
                )

        data_session.commit()


class TelegramMessageDatabaseManager:
    """Telegram Message Database Manager."""

    @staticmethod
    def get_all_messages_from_group(group_id: int, order_by_desc: bool = False) -> List[TelegramMessageOrmEntity]:
        """Return all Messages from a Single Group."""
        select_statement: Select = select(TelegramMessageOrmEntity).where(TelegramMessageOrmEntity.group_id == group_id)

        if order_by_desc:
            select_statement = select_statement.order_by(desc('date_time'))

        return cast(
            List[TelegramMessageOrmEntity],
            data_session.execute(select_statement).scalars().all()
            )

    @staticmethod
    def insert(entity_values: Dict) -> None:
        """Insert or Update one Telegram Message."""
        data_session.execute(
            insert(TelegramMessageOrmEntity).
            values(entity_values)
            )

        data_session.commit()

    @staticmethod
    def get_max_id_from_group(group_id: int) -> Optional[int]:
        """Return the Maximum id from a Group."""
        row: Optional[Row] = data_session.execute(
            select(TelegramMessageOrmEntity)
            .where(TelegramMessageOrmEntity.group_id == group_id)
            .order_by(desc('id'))
            .limit(1)
            ).one_or_none()

        if row is None:
            return None

        return int(row[0].id)


class TelegramUserDatabaseManager:
    """Telegram User Database Manager."""

    @staticmethod
    def get_by_id(pk: Optional[int]) -> Optional[TelegramUserOrmEntity]:
        """Retrieve one TelegramUserOrmEntity by PK."""
        if pk is None:
            return None

        return cast(
            Optional[TelegramUserOrmEntity],
            data_session.get(TelegramUserOrmEntity, pk)
            )

    @staticmethod
    def insert_or_update(values: Dict) -> None:
        """Insert or Update one Telegram User."""
        TelegramUserDatabaseManager.__insert_or_update_single_entity(values)
        data_session.commit()

    @staticmethod
    def insert_or_update_batch(values: Optional[List[Dict]]) -> None:
        """Insert or Update one Telegram User."""
        if values is None:
            return

        _ = [TelegramUserDatabaseManager.__insert_or_update_single_entity(item) for item in values]
        data_session.commit()

    @staticmethod
    def __insert_or_update_single_entity(entity_values: Dict) -> None:
        """Insert or Update one Telegram User."""
        is_update: bool = True
        entity: Optional[TelegramUserOrmEntity] = TelegramUserDatabaseManager.get_by_id(entity_values['id'])
        if entity is None:
            entity = TelegramUserOrmEntity(id=entity_values['id'])
            is_update = False

        if is_update:
            data_session.execute(
                update(TelegramUserOrmEntity).
                where(TelegramUserOrmEntity.id == entity_values['id']).
                values(entity_values)
                )
        else:
            data_session.execute(
                insert(TelegramUserOrmEntity).
                values(entity_values)
                )


class TelegramMediaDatabaseManager:
    """Telegram Media Database Manager."""

    @staticmethod
    def get_by_id(pk: Optional[int]) -> Optional[TelegramMediaOrmEntity]:
        """Retrieve one TelegramUserOrmEntity by PK."""
        if pk is None:
            return None

        return cast(
            Optional[TelegramMediaOrmEntity],
            data_session.get(TelegramMediaOrmEntity, pk)
            )

    @staticmethod
    def insert(entity_values: Dict) -> int:
        """Insert or Update one Telegram User."""
        cursor: CursorResult = data_session.execute(  # type:ignore
            insert(TelegramMediaOrmEntity).
            values(entity_values)
            )

        data_session.commit()

        return int(cursor.inserted_primary_key[0])
