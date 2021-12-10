"""State File Handle."""
from typing import cast

from datetime import datetime

import pytz

from TEx.models.database.temp_db_models import StateFileOrmEntity
from TEx.database.db_manager import DbManager


class StateFileHandler:
    """State File Handler."""

    @staticmethod
    def file_exist(path: str) -> bool:
        """
        Return if a File Exists.

        :param path: File Path
        :return:
        """
        return bool(DbManager.SESSIONS['temp'].query(StateFileOrmEntity).filter_by(path=path).count() > 0)

    @staticmethod
    def read_file_text(path: str) -> str:
        """Read All File Content.

        :param path: File Path
        :return: File Content
        """
        entity: StateFileOrmEntity = cast(StateFileOrmEntity, DbManager.SESSIONS['temp'].query(StateFileOrmEntity).filter_by(path=path).first())
        return str(entity.data)

    @staticmethod
    def write_file_text(path: str, content: str) -> None:
        """Write Text Content into File.

        :param path: File Path
        :param content: File Content
        :param validate_seconds: File Validation in Seconds
        :return: None
        """
        # Delete if Exists
        DbManager.SESSIONS['temp'].execute(
            StateFileOrmEntity.__table__.delete().where(StateFileOrmEntity.path == path)
            )

        entity: StateFileOrmEntity = StateFileOrmEntity(
            path=path,
            data=content,
            created_at=int(datetime.now(tz=pytz.UTC).timestamp())
            )
        DbManager.SESSIONS['temp'].add(entity)

        # Execute
        DbManager.SESSIONS['temp'].flush()
        DbManager.SESSIONS['temp'].commit()
