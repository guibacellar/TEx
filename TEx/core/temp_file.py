"""Temp File Handle."""

from typing import cast

from datetime import datetime

import pytz

from TEx.models.database.temp_db_models import TempDataOrmEntity
from TEx.database.db_manager import DbManager


class TempFileHandler:
    """Temporary File Hander."""

    @staticmethod
    def file_exist(path: str) -> bool:
        """Return if a File Exists.

        :param path: File Path
        :return:
        """
        return (
            DbManager.SESSIONS['temp']
            .query(TempDataOrmEntity)
            .filter_by(path=path)
            .count()
            > 0
        )

    @staticmethod
    def read_file_text(path: str) -> str:
        """Read All File Content.

        :param path: File Path
        :return: File Content
        """
        entity: TempDataOrmEntity = cast(TempDataOrmEntity,
                                         DbManager.SESSIONS['temp'].query(TempDataOrmEntity).filter_by(
                                             path=path).first())
        return str(entity.data)

    @staticmethod
    def remove_expired_entries() -> int:
        """Remove all Expired Entries."""
        total: int = DbManager.SESSIONS['temp'].execute(
            TempDataOrmEntity.__table__.delete().where(
                TempDataOrmEntity.valid_at <= int(datetime.now(tz=pytz.UTC).timestamp())
            )
        ).rowcount

        DbManager.SESSIONS['temp'].flush()
        DbManager.SESSIONS['temp'].commit()
        return total

    @staticmethod
    def purge() -> int:
        """Remove all Entries."""
        total: int = DbManager.SESSIONS['temp'].execute(TempDataOrmEntity.__table__.delete()).rowcount
        DbManager.SESSIONS['temp'].flush()
        DbManager.SESSIONS['temp'].commit()
        return total

    @staticmethod
    def write_file_text(path: str, content: str, validate_seconds: int = 3600) -> None:
        """
        Write Text Content into File.

        :param path: File Path
        :param content: File Content
        :param validate_seconds: File Validation in Seconds
        :return: None
        """
        # Delete if Exists
        DbManager.SESSIONS['temp'].execute(
            TempDataOrmEntity.__table__.delete().where(TempDataOrmEntity.path == path)
        )

        entity: TempDataOrmEntity = TempDataOrmEntity(
            path=path,
            data=content,
            created_at=int(datetime.now(tz=pytz.UTC).timestamp()),
            valid_at=int(datetime.now(tz=pytz.UTC).timestamp()) + validate_seconds
        )
        DbManager.SESSIONS['temp'].add(entity)

        # Execute
        DbManager.SESSIONS['temp'].flush()
        DbManager.SESSIONS['temp'].commit()
