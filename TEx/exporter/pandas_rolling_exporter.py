"""Pandas Rolling Data Exporter."""
from __future__ import annotations

import logging
import os
from configparser import SectionProxy
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pandas as pd
import pytz

from TEx.exporter.exporter_base import BaseExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity

logger = logging.getLogger('TelegramExplorer')


class PandasRollingExporter(BaseExporter):
    """Basic Pandas Rolling Exporter."""

    __DEFAULT_FIELD_PATTERN: str = 'date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on'

    def __init__(self) -> None:
        """Initialize the Exporter."""
        super().__init__()
        self.rolling_every_minutes: int = 0
        self.fields: List[str] = []
        self.use_header: bool = False
        self.export_format: str = 'csv'
        self.current_df: pd.DataFrame
        self.actual_rounded_time: datetime = datetime.now(tz=pytz.UTC)
        self.keep_last_files: int = 0
        self.source_phone: str = ''

    def __configure_dataframe(self) -> None:
        """Initialize and Configure the Dataframe."""
        self.current_df = pd.DataFrame(
            columns=self.fields,
        )

    def configure(self, config: SectionProxy, source: str) -> None:
        """Configure the Exporter."""
        self.rolling_every_minutes = int(config.get('rolling_every_minutes', fallback='30'))
        self.use_header = config.get('use_header', fallback='true') == 'true'
        self.fields = config.get('fields', fallback=PandasRollingExporter.__DEFAULT_FIELD_PATTERN).split(',')
        self.export_format = config.get('output_format', fallback='csv')
        self.keep_last_files = int(config.get('keep_last_files', fallback='20'))
        self.source_phone = source.replace('+', '')

        super().configure_base(config=config)

        # Set DataFrame
        self.__configure_dataframe()

        # Compute the First Rounded Time
        current_dt: datetime = datetime.now(tz=pytz.UTC)
        self.actual_rounded_time = current_dt - timedelta(
            minutes=current_dt.minute % self.rolling_every_minutes,
            seconds=current_dt.second,
            microseconds=current_dt.microsecond,
        )

    def __rolling(self) -> None:
        """Run Rolling Logic."""
        # Compute the Normalized Rounded Time
        current_dt: datetime = datetime.now(tz=pytz.UTC)
        current_rounded_time: datetime = current_dt - timedelta(
            minutes=current_dt.minute % self.rolling_every_minutes,
            seconds=current_dt.second,
            microseconds=current_dt.microsecond,
        )

        # Check if it needs to Roll the File
        if self.actual_rounded_time != current_rounded_time:

            # Flush to Disk
            self.__flush()

            # Reset the DF
            self.current_df.drop(self.current_df.index, inplace=True)

            # Update Actual Rounded Time
            self.actual_rounded_time = current_rounded_time

            # Remove Old Files
            self._keep_last_files_only(directory_path=self.file_root_path, file_count=self.keep_last_files)

    def __flush(self) -> None:
        """Flush DF to Disc."""
        file_name: str = os.path.join(self.file_root_path, f"tex_export_{self.source_phone}_{self.actual_rounded_time.strftime('%Y%m%d%H%M')}")

        if self.export_format == 'csv':
            file_name += '.csv'
            self.__ensure_file_not_exists(file_path=file_name)
            self.current_df.to_csv(file_name, index=False, header=self.use_header, mode='w')

        elif self.export_format == 'xml':
            file_name += '.xml'
            self.__ensure_file_not_exists(file_path=file_name)
            self.current_df.to_xml(file_name, index=False, root_name='TEx')

        elif self.export_format == 'json':
            file_name += '.json'
            self.__ensure_file_not_exists(file_path=file_name)
            self.current_df.to_json(file_name, orient='records', date_format='iso', indent=0)

        elif self.export_format == 'pickle':
            file_name += '.bin'
            self.__ensure_file_not_exists(file_path=file_name)
            self.current_df.to_pickle(file_name)

        # Log File Rolling
        logger.info(f'\t\t\t Writing Export File at {file_name}')

    def __ensure_file_not_exists(self, file_path: str) -> None:
        """Ensure the File not Exists. If exists, rename previous file. Note: CHAT GPT-4 Assisted Code."""
        if not os.path.exists(file_path):
            return

        base_name, extension = os.path.splitext(file_path)
        counter: int = 1
        new_filename: str = f'{base_name}_{counter}{extension}'

        # Iterate Until have no Conflicted File
        while os.path.exists(new_filename):
            counter += 1
            new_filename = f'{base_name}_{counter}{extension}'

        # Rename File
        Path(file_path).rename(new_filename)

    async def run(self, entity: FinderNotificationMessageEntity, rule_id: str) -> None:
        """Run the Exporting Process."""
        # Run Rolling Logic
        self.__rolling()

        # Add Data to Dataframe
        self.current_df.loc[len(self.current_df)] = entity.model_dump(include=self.fields)  # type: ignore

    def shutdown(self) -> None:
        """Gracefully Shutdown the Exporter and Flush All Remaining Data into Disk."""
        self.__flush()

        # Remove Old Files
        self._keep_last_files_only(directory_path=self.file_root_path, file_count=self.keep_last_files)
