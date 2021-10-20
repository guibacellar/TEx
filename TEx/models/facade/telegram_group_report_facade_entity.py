"""Facade Entity for Report Generation."""

from TEx.models.database.telegram_db_model import TelegramGroupOrmEntity


class TelegramGroupReportFacadeEntity:  # pylint: disable=R0902
    """Facade Entity for Report Generation."""

    id: int  # noqa: A003
    constructor_id: str
    access_hash: str
    group_username: str
    title: str

    fake: bool
    gigagroup: bool
    has_geo: bool
    restricted: bool
    scam: bool
    verified: bool

    participants_count: int

    photo_id: int
    photo_base64: str
    photo_name: str

    source: str

    meta_message_count: int


class TelegramGroupReportFacadeEntityMapper:
    """Mapper for TelegramGroupReportFacadeEntity."""

    @staticmethod
    def create_from_dbentity(source: TelegramGroupOrmEntity) -> TelegramGroupReportFacadeEntity:
        """Map TelegramGroupOrmEntity to TelegramGroupReportFacadeEntity."""
        h_result: TelegramGroupReportFacadeEntity = TelegramGroupReportFacadeEntity()

        h_result.id = source.id
        h_result.constructor_id = source.constructor_id
        h_result.access_hash = source.access_hash
        h_result.group_username = source.group_username
        h_result.title = source.title

        h_result.fake = source.fake
        h_result.gigagroup = source.gigagroup
        h_result.has_geo = source.has_geo
        h_result.restricted = source.restricted
        h_result.scam = source.scam
        h_result.verified = source.verified

        h_result.participants_count = source.participants_count

        h_result.photo_id = source.photo_id
        h_result.photo_base64 = source.photo_base64
        h_result.photo_name = source.photo_name

        h_result.source = source.source

        return h_result
