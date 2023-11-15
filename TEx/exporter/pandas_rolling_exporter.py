"""Pandas Rolling Data Exporter."""
from __future__ import annotations

import os.path
from configparser import SectionProxy
from typing import Dict, List, Optional, Union

from datetime import datetime, timedelta
import pandas as pd

from TEx.exporter.exporter_base import BaseExporter
from TEx.models.facade.finder_notification_facade_entity import FinderNotificationMessageEntity


class PandasRollingExporter(BaseExporter):
    """Basic Pandas Rolling Exporter."""

    __DEFAULT_FIELD_PATTERN: str = 'date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on'
    __AUTO_FLUSH_MESSAGE_COUNT: int = 20

    def __init__(self) -> None:
        """Initialize the Exporter."""
        super().__init__()
        self.rolling_every_minutes: int
        self.fields: List[str] = []
        self.use_header: bool
        self.export_format: str
        self.current_df: pd.DataFrame

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

    def __rolling(self) -> None:
        """Run Rolling Logic."""

    async def run(self, entity: FinderNotificationMessageEntity, rule_id: str, source: str) -> None:
        pass
        # """Run the Export Process."""
        # self.__rolling()
        #
        # # Add Data to Dataframe
        # self.current_df.loc[len(self.current_df)] = entity.model_dump(include=self.fields)
        #
        # current_time = datetime.now()
        # rounded_time = current_time - timedelta(minutes=current_time.minute % self.rolling_every_minutes,
        #                                         seconds=current_time.second,
        #                                         microseconds=current_time.microsecond)
        #
        # # Formata o timestamp para usar no nome do arquivo
        # file_name = os.path.join(self.file_root_path, f"data_{rounded_time.strftime('%Y%m%d%H%M')}.csv")
        #
        # # Salva o DataFrame no arquivo CSV
        # self.current_df.to_csv(file_name, index=False, header=self.use_header)
        # print(f"DataFrame salvo em: {file_name}")
