"""TEx Database Initializer."""
from TEx.models.database.telegram_db_model import TelegramDataBaseDeclarativeBase
from TEx.models.database.temp_db_models import TempDataBaseDeclarativeBase

from TEx.database import SQLALCHEMY_BINDS


class DbInitializer:
    """Central Database Initializer."""

    @staticmethod
    def init() -> None:
        """Initialize DB and Structure."""
        TempDataBaseDeclarativeBase.metadata.create_all(SQLALCHEMY_BINDS['temp'])
        TelegramDataBaseDeclarativeBase.metadata.create_all(SQLALCHEMY_BINDS['data'])
