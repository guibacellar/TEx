"""TEx - Telegram Explorer.

By: Th3 0bservator
"""
import asyncio
import importlib
import logging
import logging.config
import os
import sys
import types
from configparser import ConfigParser
from typing import Dict, List, Optional

import toml

from TEx.core.base_module import BaseModule

logger = logging.getLogger('TelegramExplorer')

VERSION: str = toml.load(os.path.join('..', 'pyproject.toml'))['tool']['poetry']['version']

BANNER: str = f'''
TEx - Telegram Explorer
Version {VERSION}
By: Th3 0bservator
'''  # pylint: disable=R1732


class TelegramMonitorRunner:
    """OSIx Main Module."""

    MODULE_SUPRESS_LIST: List = [
        'input_args_handler.py',
        'state_file_handler.py',
        'temp_file_manager.py',
        '__init__.py',
        '__pycache__'
    ]
    """List of Modules to Suppress on SysOut Report"""

    def __init__(self) -> None:
        """Initialize Module."""
        self.config: Optional[ConfigParser] = None
        self.available_modules: List[str] = []

    def main(self) -> int:
        """Application Entrypoint."""
        self.__setup_logging()

        logger.info(BANNER)

        if not self.check_python_version():
            return 1

        self.__load_settings()
        self.__list_modules()

        if not self.config:
            return -1

        # Load Modules
        args: Dict = {}
        data: Dict = {'internals': {'panic': False}}

        # Execute Pre Pipeline
        self.__execute_sequence(args, data, self.config['PIPELINE']['pre_pipeline_sequence'].split('\n'),
                                'Initialization')

        # Execute Pipeline
        self.__execute_sequence(args, data, self.config['PIPELINE']['pipeline_sequence'].split('\n'), 'Pipeline')

        # Execute Post Pipeline
        self.__execute_sequence(args, data, self.config['PIPELINE']['post_pipeline_sequence'].split('\n'),
                                'Termination')

        return 0

    def __execute_sequence(self, args: Dict, data: Dict, sequence_spec: List, sequence_name: str) -> None:

        # Check Panic Exit Control
        if data['internals']['panic']:
            return

        logger.info(f'[*] Executing {sequence_name}:')
        loop = asyncio.get_event_loop()

        if self.config is None:
            logger.fatal('[?] Unknown Config Parser')
            raise Exception("Unknown Config Parser")  # pylint: disable=W0719

        for pipeline_item in sequence_spec:

            if pipeline_item == '' or data['internals']['panic']:
                continue

            pipeline_item_meta: List[str] = pipeline_item.split('.')

            osix_module: types.ModuleType = importlib.import_module(f'modules.{".".join(pipeline_item_meta[:-1])}')
            module_instance: BaseModule = getattr(osix_module, pipeline_item_meta[-1])()

            loop.run_until_complete(
                self.__execute_pipeline_item(args, data, module_instance, pipeline_item)
            )

    async def __execute_pipeline_item(self, args: Dict, data: Dict, module_instance: BaseModule,
                                      pipeline_item: str) -> None:

        if not self.config:
            return

        # Check Module Activation
        can_activate_module: bool = await module_instance.can_activate(
            config=self.config,
            args=args,
            data=data
        )

        if not can_activate_module:
            return

        logger.info(f'\t[+] {pipeline_item}')

        # Execute Module
        await module_instance.run(
            config=self.config,
            args=args,
            data=data
        )

    def check_python_version(self) -> bool:
        """Check if the Current Python Version is Supported."""
        # Check Python Requirements
        major = sys.version_info[0]
        minor = sys.version_info[1]

        python_version = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}.{str(sys.version_info[2])}"

        # Python Deprecated Version Check
        if major != 3 or minor <= 9:
            logger.warning(
                '**** Python 3.8 and Python 3.9 is deprecated. Please, consider upgrade your Python runtime version. **** ')
            logger.fatal(f'Current Installed Version is: {python_version}')

        return True

    def __setup_logging(self) -> None:
        """Setups Log Config."""
        logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'logging.conf'))
        logging.getLogger('telethon').setLevel(level=logging.WARNING)

    def __list_modules(self) -> None:
        """
        List All Available Modules.

        :return: None
        """
        # Check Modules
        logger.info('[*] Installed Modules:')
        for file in sorted(os.listdir(os.path.join(os.path.dirname(__file__), 'modules'))):
            if file not in TelegramMonitorRunner.MODULE_SUPRESS_LIST:
                logger.info(f'\t{file}')

    def __load_settings(self) -> None:
        """
        Load the config.ini file into Settings Object.

        :return: None
        """
        logger.info('[*] Loading Configurations:')
        self.config = ConfigParser()
        self.config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
