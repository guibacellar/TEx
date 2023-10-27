"""TEx Database Initializer."""
from TEx.database.db_manager import DbManager
from TEx.database.db_migration import DatabaseMigrator
from TEx.models.database.telegram_db_model import TelegramDataBaseDeclarativeBase
from TEx.models.database.temp_db_models import TempDataBaseDeclarativeBase


class DbInitializer:
    """Central Database Initializer."""

    @staticmethod
    def init(data_path: str) -> None:
        """Initialize DB and Structure."""
        # Initialize Main DB
        DbManager.init_db(data_path=data_path)

        # Initialize Main DB
        TempDataBaseDeclarativeBase.metadata.create_all(DbManager.SQLALCHEMY_BINDS['temp'], checkfirst=True)
        TelegramDataBaseDeclarativeBase.metadata.create_all(DbManager.SQLALCHEMY_BINDS['data'], checkfirst=True)

        # Migrations
        DatabaseMigrator.apply_migrations()
