"""Pandas Rolling Data Exporter."""
from __future__ import annotations

import os.path
import logging
from configparser import SectionProxy
from typing import List

from datetime import datetime, timedelta
import pandas as pd
import pytz

from TEx.exporter.exporter_base import BaseExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity

logger = logging.getLogger('TelegramExplorer')


class PandasRollingExporter(BaseExporter):
    """Basic Pandas Rolling Exporter."""

    __DEFAULT_FIELD_PATTERN: str = 'date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on'

    # TODO: Implements Auto Flush, LOL

    def __init__(self) -> None:
        """Initialize the Exporter."""
        super().__init__()
        self.rolling_every_minutes: int = 0
        self.fields: List[str] = []
        self.use_header: bool = False
        self.export_format: str = 'csv'
        self.current_df: pd.DataFrame
        self.actual_rounded_time: datetime = datetime.now(tz=pytz.UTC)

    def __configure_dataframe(self) -> None:
        """Initialize and Configure the Dataframe."""
        self.current_df = pd.DataFrame(
            columns=self.fields
        )

    def configure(self, config: SectionProxy) -> None:
        """Configure the Exporter."""
        self.rolling_every_minutes = int(config.get('rolling_every_minutes', fallback='30'))
        self.use_header = config.get('use_header', fallback='true') == 'true'
        self.fields = config.get('fields', fallback=PandasRollingExporter.__DEFAULT_FIELD_PATTERN).split(',')
        self.export_format = config.get('output_format', fallback='csv')

        super().configure_base(config=config)

        # Set DataFrame
        self.__configure_dataframe()

        # Compute the First Rounded Time
        current_dt: datetime = datetime.now(tz=pytz.UTC)
        self.actual_rounded_time: datetime = current_dt - timedelta(
            minutes=current_dt.minute % self.rolling_every_minutes,
            seconds=current_dt.second,
            microseconds=current_dt.microsecond
        )

    def __rolling(self) -> None:
        """Run Rolling Logic."""
        # Compute the Normalized Rounded Time
        current_dt: datetime = datetime.now(tz=pytz.UTC)
        current_rounded_time: datetime = current_dt - timedelta(
            minutes=current_dt.minute % self.rolling_every_minutes,
            seconds=current_dt.second,
            microseconds=current_dt.microsecond
        )

        # Check if it needs to Roll the File
        if self.actual_rounded_time != current_rounded_time:

            # Flush to Disk
            self.__flush()

            # Reset the DF
            self.current_df.drop(self.current_df.index, inplace=True)

            # Update Actual Rounded Time
            self.actual_rounded_time = current_rounded_time

    def __flush(self) -> None:
        """Flush DF to Disc."""
        file_name: str = os.path.join(self.file_root_path, f"tex_export_{self.actual_rounded_time.strftime('%Y%m%d%H%M')}")

        if self.export_format == 'csv':
            file_name += '.csv'
            self.current_df.to_csv(file_name, index=False, header=self.use_header, mode='w')

        elif self.export_format == 'xml':
            file_name += '.xml'
            self.current_df.to_xml(file_name, index=False, root_name='TEx')

        elif self.export_format == 'json':
            file_name += '.json'
            self.current_df.to_json(file_name, orient='records', date_format='iso', indent=0, )

        elif self.export_format == 'pickle':
            file_name += '.bin'
            self.current_df.to_pickle(file_name)

        # Log File Rolling
        logger.info(f'\t\t\t Writing Export File at {file_name}')

        # TODO: Check if FIle Exists, and Creates a Next One (EX: _v2, _v3, and So One)

        # TODO: Control to Keep the Latest X Files

        # TODO: Add the SOURCE PHONE to File Name (Allow to Keep Multiple Phones/Processes in Same Directory)

    async def run(self, entity: FinderNotificationMessageEntity, rule_id: str, source: str) -> None:

        # Run Rolling Logic
        self.__rolling()

        # Add Data to Dataframe
        self.current_df.loc[len(self.current_df)] = entity.model_dump(include=self.fields)

    def shutdown(self) -> None:
        """Gracefully Shutdown the Exporter and Flush All Remaining Data into Disk."""
        self.__flush()
