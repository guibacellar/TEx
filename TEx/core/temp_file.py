"""Temp File Handle."""

from typing import cast

from datetime import datetime

import pytz

from TEx.models.database.temp_db_models import TempDataOrmEntity
from TEx.database import temp_session


class TempFileHandler:
    """Temporary File Hander."""

    @staticmethod
    def file_exist(path: str) -> bool:
        """Return if a File Exists.

        :param path: File Path
        :return:
        """
        return bool(temp_session.query(TempDataOrmEntity).filter_by(path=path).count() > 0)

    @staticmethod
    def read_file_text(path: str) -> str:
        """Read All File Content.

        :param path: File Path
        :return: File Content
        """
        entity: TempDataOrmEntity = cast(TempDataOrmEntity, temp_session.query(TempDataOrmEntity).filter_by(path=path).first())
        return str(entity.data)

    @staticmethod
    def remove_expired_entries() -> int:
        """Remove all Expired Entries."""
        total: int = temp_session.execute(  # type:ignore
            TempDataOrmEntity.__table__.delete().where(
                TempDataOrmEntity.valid_at <= int(datetime.now(tz=pytz.UTC).timestamp())
                )
            ).rowcount

        temp_session.flush()
        temp_session.commit()
        return total

    @staticmethod
    def purge() -> int:
        """Remove all Entries."""
        total: int = temp_session.execute(TempDataOrmEntity.__table__.delete()).rowcount  # type:ignore
        temp_session.flush()
        temp_session.commit()
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
        temp_session.execute(
            TempDataOrmEntity.__table__.delete().where(TempDataOrmEntity.path == path)
            )

        entity: TempDataOrmEntity = TempDataOrmEntity(
            path=path,
            data=content,
            created_at=int(datetime.now(tz=pytz.UTC).timestamp()),
            valid_at=int(datetime.now(tz=pytz.UTC).timestamp()) + validate_seconds
            )
        temp_session.add(entity)

        # Execute
        temp_session.flush()
        temp_session.commit()
