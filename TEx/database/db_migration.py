"""DB Migrator."""
from __future__ import annotations

import logging

import sqlalchemy
from sqlalchemy import Index, MetaData, Table

from TEx.database.db_manager import DbManager
from TEx.models.database.telegram_db_model import TelegramMediaOrmEntity, TelegramMessageOrmEntity

logger = logging.getLogger('TelegramExplorer')


class DatabaseMigrator:
    """Global Telegram DB Declarative Base."""

    @staticmethod
    def apply_migrations() -> None:
        """Apply all Migrations."""
        # Check Data Copy Migration to Shards
        for db_name in ['data']:
            DatabaseMigrator.__apply_migration_for_bind(db_name=db_name)

    @staticmethod
    def __apply_migration_for_bind(db_name: str) -> None:
        """Apply Migrations."""
        meta: MetaData = sqlalchemy.MetaData()
        meta.reflect(bind=DbManager.SQLALCHEMY_BINDS[db_name])

        # ix_telegram_message_group_id_date - V0.3.0
        DatabaseMigrator.__create_index(
            metadata=meta,
            table_name='telegram_message',
            index_name='ix_telegram_message_group_id_date',
            version='V0.3.0',
            field_spec=(TelegramMessageOrmEntity.group_id, TelegramMessageOrmEntity.date_time.desc()),
            db_name=db_name,
        )

        # ix_telegram_media_group_id_date - V0.3.0
        DatabaseMigrator.__create_index(
            metadata=meta,
            table_name='telegram_media',
            index_name='ix_telegram_media_group_id_date',
            version='V0.3.0',
            field_spec=(TelegramMediaOrmEntity.group_id, TelegramMediaOrmEntity.date_time.desc()),
            db_name=db_name,
        )

    @staticmethod
    def __create_index(metadata: MetaData, table_name: str, index_name: str, version: str, field_spec: tuple,
                       db_name: str) -> None:

        # Messages Table
        table: Table = metadata.tables[table_name]

        # ix_telegram_message_group_id_date - V0.3.0
        index_exists: bool = DatabaseMigrator.__check_index_exists(
            table=table,
            index_name=index_name,
        )

        if not index_exists:
            logger.info(f'\t[*] APPLYING DB ({db_name}) MIGRATION ({version}) - {index_name}')

            new_index: Index = sqlalchemy.Index(
                index_name,
                *field_spec,
            )
            new_index.create(bind=DbManager.SQLALCHEMY_BINDS[db_name])

    @staticmethod
    def __check_index_exists(table: Table, index_name: str) -> bool:
        """Check if Index Exists on Table."""
        return len([item for item in table.indexes if item.name == index_name]) == 1
