"""Facade Entity for Report Generation."""

import datetime
from typing import Optional

from TEx.models.database.telegram_db_model import TelegramMessageOrmEntity


class TelegramMessageReportFacadeEntity:  # pylint: disable=R0902
    """Facade Entity for Report Generation."""

    id: int  # noqa: A003
    group_id: int
    media_id: Optional[int]

    date_time: datetime.datetime
    message: str
    raw: str

    from_id: int
    from_type: str
    to_id: int

    meta_next: bool
    meta_previous: bool


class TelegramMessageReportFacadeEntityMapper:
    """Mapper for TelegramMessageReportFacadeEntity."""

    @staticmethod
    def create_from_dbentity(source: TelegramMessageOrmEntity) -> TelegramMessageReportFacadeEntity:
        """Map TelegramMessageOrmEntity to TelegramMessageReportFacadeEntity."""
        h_result: TelegramMessageReportFacadeEntity = TelegramMessageReportFacadeEntity()

        h_result.id = source.id
        h_result.group_id = source.group_id
        h_result.media_id = source.media_id
        h_result.date_time = source.date_time
        h_result.message = source.message
        h_result.raw = source.raw
        h_result.from_id = source.from_id
        h_result.from_type = source.from_type
        h_result.to_id = source.to_id

        return h_result
