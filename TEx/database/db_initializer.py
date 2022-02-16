"""TEx Database Initializer."""
import sqlalchemy

from TEx.database.telegram_group_database import TelegramGroupDatabaseManager
from TEx.models.database.telegram_db_model import TelegramDataBaseDeclarativeBase, TelegramMediaDataBaseDeclarativeBase
from TEx.models.database.temp_db_models import TempDataBaseDeclarativeBase
from typing import Dict

from TEx.database.db_manager import DbManager


class DbInitializer:
    """Central Database Initializer."""

    @staticmethod
    def init(data_path: str, args: Dict) -> None:
        """Initialize DB and Structure."""

        # Initialize Main DB
        DbManager.init_db(data_path=data_path)

        # Initialize Main DB
        TempDataBaseDeclarativeBase.metadata.create_all(DbManager.SQLALCHEMY_BINDS['temp'])
        TelegramDataBaseDeclarativeBase.metadata.create_all(DbManager.SQLALCHEMY_BINDS['data'])

        DbInitializer.init_media_dbs(data_path=data_path, args=args)

    @staticmethod
    def init_media_dbs(data_path: str, args: Dict):
        """Initialize the Media DB's."""

        # Initialize Media Databases
        if 'target_phone_number' in args and args['target_phone_number']:
            for group in TelegramGroupDatabaseManager.get_all_by_phone_number(args['target_phone_number']):
                DbManager.init_media_db(group_id=str(group.id), data_path=data_path)
                TelegramMediaDataBaseDeclarativeBase.metadata.create_all(DbManager.SQLALCHEMY_BINDS[f'media_{str(group.id)}'])

                # Upgrade Table Schema - idx_dt_mt
                DbManager.SQLALCHEMY_BINDS[f'media_{str(group.id)}'].execute(
                    sqlalchemy.DDL('''CREATE INDEX IF NOT EXISTS idx_dt_mt ON telegram_media (date_time, mime_type);''')
                )
