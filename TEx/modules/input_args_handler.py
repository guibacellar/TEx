"""Input Arguments Handler."""

import argparse
import logging
from configparser import ConfigParser
from typing import Dict

from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class InputArgsHandler(BaseModule):
    """Module That Handle the Input Arguments."""

    __ARGS: Dict = {
        'connect': {
            'help': 'Create the Connection to the Telegram Servers and Store the Authentication',
            'sub_args': {
                'api_id': {
                    'param': '--api_id', 'type': str, 'action': 'store', 'help': 'Telegram API ID.',
                    'default': None, 'required': True,
                    },
                'api_hash': {
                    'param': '--api_hash', 'type': str, 'action': 'store', 'help': 'Telegram API Hash.',
                    'default': None, 'required': True
                    },
                'target_phone_number': {
                    'param': '--phone_number', 'type': str, 'action': 'store', 'help': 'Telegram Account Phone Number',
                    'default': None, 'required': True
                    },
                'data_path': {
                    'param': '--data_path', 'type': str, 'action': 'store', 'help': 'Database Location Path',
                    'default': None, 'required': True
                    },
                }
            },
        'load_groups': {
            'help': 'Download and Refresh Groups and Members List',
            'sub_args': {
                'target_phone_number': {
                    'param': '--phone_number', 'type': str, 'action': 'store', 'help': 'Telegram Account Phone Number',
                    'default': None, 'required': True
                    },
                'refresh_profile_photos': {
                    'param': '--refresh_profile_photos', 'type': str, 'action': 'store_true', 'help': 'Force to Refresh all Profile Photos',
                    'default': False, 'required': False
                    },
                'data_path': {
                    'param': '--data_path', 'type': str, 'action': 'store', 'help': 'Database Location Path',
                    'default': None, 'required': True
                    },
                }
            },
        'download_messages': {
            'help': 'Download Message History',
            'sub_args': {
                'target_phone_number': {
                    'param': '--phone_number', 'type': str, 'action': 'store', 'help': 'Telegram Account Phone Number',
                    'default': None, 'required': True
                    },
                'ignore_media': {
                    'param': '--ignore_media', 'type': str, 'action': 'store_true', 'help': 'Set to do not Download Media from Messages',
                    'default': False, 'required': False
                    },
                'data_path': {
                    'param': '--data_path', 'type': str, 'action': 'store', 'help': 'Database Location Path',
                    'default': None, 'required': True
                    },
                }
            },
        'report': {
            'help': 'Generate the Report with all Messages and Medias',
            'sub_args': {
                'target_phone_number': {
                    'param': '--phone_number', 'type': str, 'action': 'store', 'help': 'Telegram Account Phone Number',
                    'default': None, 'required': True
                    },
                'order_desc': {
                    'param': '--order_desc', 'type': str, 'action': 'store_true',
                    'help': 'Set the Date/Time Order to Descending',
                    'default': False, 'required': False
                    },
                'filter': {
                    'param': '--filter', 'type': str, 'action': 'store',
                    'help': 'Filter Terms',
                    'default': None, 'required': False
                    },
                'limit_days': {
                    'param': '--limit_days', 'type': int, 'action': 'store',
                    'help': 'Limit Messages Period in Days',
                    'default': 3650, 'required': False
                    },
                'report_folder': {
                    'param': '--report_folder', 'type': str, 'action': 'store',
                    'help': 'Set the Report Output Folder',
                    'default': 'reports', 'required': False
                    },
                'around_messages': {
                    'param': '--around_messages', 'type': int, 'action': 'store',
                    'help': 'Number of Messages to be Returned Around (Previous and After) the Message that was been filtered. Works together --filter',
                    'default': 1, 'required': False
                    },
                'group_id': {
                    'param': '--group_id', 'type': str, 'action': 'store',
                    'help': 'Target Group IDs. Ex: --group GroupA,GroupB,"Group C"',
                    'default': '*', 'required': False
                    },
                'data_path': {
                    'param': '--data_path', 'type': str, 'action': 'store', 'help': 'Database Location Path',
                    'default': None, 'required': True
                    },
                }
            },
        'purge_temp_files': {
            'param': '--purge_temp_files',
            'type': str,
            'action': 'store_true',
            'help': 'Force Delete All Temporary Files',
            'default': False,
            'required': False,
            'sub_args': {
                'data_path': {
                    'param': '--data_path', 'type': str, 'action': 'store', 'help': 'Database Location Path',
                    'default': None, 'required': True
                    },
                }
            }
        }

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        parent_parser = argparse.ArgumentParser(description=f'TEx - Telegram Monitor - {open("../__version__.txt").read()}')
        sub_parser = parent_parser.add_subparsers(title='actions', dest='action')

        # Add Parameters to Arg Parser
        for arg in InputArgsHandler.__ARGS:
            spec: Dict = InputArgsHandler.__ARGS[arg]

            parser_sub_command = sub_parser.add_parser(arg, help=spec['help'])

            for sub_arg in spec['sub_args']:
                sub_arg_spec: Dict = spec['sub_args'][sub_arg]

                parser_sub_command.add_argument(
                    sub_arg_spec['param'], action=sub_arg_spec['action'], dest=sub_arg,
                    help=sub_arg_spec['help'], default=sub_arg_spec['default'], required=sub_arg_spec['required']
                    )

        # Parse Args
        input_args = parent_parser.parse_args()

        # Add to Result Args
        for arg in InputArgsHandler.__ARGS:

            args.update(
                {arg: getattr(input_args, 'action') == arg}  # noqa: B009
                )

            if args[arg]:  # Parse Only If the Action was True
                for sub_arg in InputArgsHandler.__ARGS[arg]['sub_args']:
                    args.update(
                        {sub_arg: getattr(input_args, sub_arg)}
                        )

        # Print Settings
        for key, value in args.items():
            logger.info(f'\t\t{key} = {value}')
