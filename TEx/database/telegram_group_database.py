"""Telegram Group Database Manager."""
from typing import Dict, List, Optional, cast

from sqlalchemy import desc, insert, select, update
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.sql import Select
from sqlalchemy.orm import Session

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
                .where(TelegramGroupOrmEntity.source == phone_number)
                ).scalars().all()
            )

    @staticmethod
    def get_by_id(pk: str) -> Optional[TelegramGroupOrmEntity]:
        """Retrieve one TelegramGroupOrmEntity by PK."""
        return cast(
            Optional[TelegramGroupOrmEntity],
            DbManager.SESSIONS['data'].get(TelegramGroupOrmEntity, pk)
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
            DbManager.SESSIONS['data'].execute(
                update(TelegramGroupOrmEntity).
                where(TelegramGroupOrmEntity.id == entity_values['id']).
                values(entity_values)
                )
        else:
            DbManager.SESSIONS['data'].execute(
                insert(TelegramGroupOrmEntity).
                values(entity_values)
                )

        DbManager.SESSIONS['data'].commit()


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
            DbManager.SESSIONS['data'].execute(select_statement).scalars().all()
            )

    @staticmethod
    def insert(entity_values: Dict) -> None:
        """Insert or Update one Telegram Message."""
        DbManager.SESSIONS['data'].execute(
            insert(TelegramMessageOrmEntity).
            values(entity_values)
            )
        DbManager.SESSIONS['data'].commit()

    @staticmethod
    def get_max_id_from_group(group_id: int) -> Optional[int]:
        """Return the Maximum id from a Group."""
        row: Optional[Row] = DbManager.SESSIONS['data'].execute(
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
            DbManager.SESSIONS['data'].get(TelegramUserOrmEntity, pk)
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

        if is_update:
            DbManager.SESSIONS['data'].execute(
                update(TelegramUserOrmEntity).
                where(TelegramUserOrmEntity.id == entity_values['id']).
                values(entity_values)
                )
        else:
            DbManager.SESSIONS['data'].execute(
                insert(TelegramUserOrmEntity).
                values(entity_values)
                )


class TelegramMediaDatabaseManager:
    """Telegram Media Database Manager."""

    @staticmethod
    def get_by_id(pk: Optional[int], group_id: int) -> Optional[TelegramMediaOrmEntity]:
        """Retrieve one TelegramUserOrmEntity by PK."""
        if pk is None:
            return None

        return cast(
            Optional[TelegramMediaOrmEntity],
            DbManager.SESSIONS[f'media_{str(group_id)}'].get(TelegramMediaOrmEntity, pk)
            )

    @staticmethod
    def insert(entity_values: Dict, group_id: int) -> int:
        """Insert or Update one Telegram User."""

        session: Session = DbManager.SESSIONS[f'media_{str(group_id)}']

        cursor: CursorResult = session.execute(  # type:ignore
            insert(TelegramMediaOrmEntity).
            values(entity_values)
            )
        session.commit()

        return int(cursor.inserted_primary_key[0])
