import asyncio

from sqlalchemy import delete

from TEx.core.dir_manager import DirectoryManagerUtils
from TEx.database.db_initializer import DbInitializer
from TEx.database.db_manager import DbManager
from TEx.models.database.telegram_db_model import (
    TelegramGroupOrmEntity,
    TelegramMediaOrmEntity, TelegramMessageOrmEntity, )
from TEx.modules.execution_configuration_handler import ExecutionConfigurationHandler


class TestsCommon:

    @staticmethod
    def basic_test_setup():
        """Execute Basic Tasks for Tests."""

        DirectoryManagerUtils.ensure_dir_struct('_data')
        DirectoryManagerUtils.ensure_dir_struct('_data/resources')
        DirectoryManagerUtils.ensure_dir_struct('_data/media')

        DbInitializer.init(data_path='_data/')

        # Reset SQLlite Groups
        DbManager.SESSIONS['data'].execute(delete(TelegramMessageOrmEntity))
        DbManager.SESSIONS['data'].execute(delete(TelegramGroupOrmEntity))
        DbManager.SESSIONS['data'].execute(delete(TelegramMediaOrmEntity))
        DbManager.SESSIONS['data'].commit()

    @staticmethod
    def execute_basic_pipeline_steps_for_initialization(config, args, data):

        execution_configuration_loader: ExecutionConfigurationHandler = ExecutionConfigurationHandler()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            execution_configuration_loader.run(
                config=config,
                args=args,
                data=data
            )
        )
