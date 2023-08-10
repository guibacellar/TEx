"""Input Arguments Handler."""

import argparse
import logging
from configparser import ConfigParser
from typing import Dict, List

from TEx.core.base_module import BaseModule

logger = logging.getLogger()


class InputArgsHandler(BaseModule):
    """Module That Handle the Input Arguments."""

    __ARGS: Dict = {
        'connect': {
            'help': 'Create the Connection to the Telegram Servers and Store the Authentication',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                }
            },
        'load_groups': {
            'help': 'Download and Refresh Groups and Members List',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'refresh_profile_photos': {
                    'param': '--refresh_profile_photos', 'type': str, 'action': 'store_true', 'help': 'Force to Refresh all Profile Photos',
                    'default': False, 'required': False
                    },
                }
            },
        'download_messages': {
            'help': 'Download Message History',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'ignore_media': {
                    'param': '--ignore_media', 'type': str, 'action': 'store_true', 'help': 'Set to not Download Media from Messages',
                    'default': False, 'required': False
                    },
                'group_id': {
                    'param': '--group_id', 'type': str, 'action': 'store',
                    'help': 'Target Group IDs. Ex: --group GroupA,GroupB,"Group C"',
                    'default': '*', 'required': False
                    },
                }
            },
        'listen': {
            'help': 'Actively Listen all Chats',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'ignore_media': {
                    'param': '--ignore_media', 'type': str, 'action': 'store_true',
                    'help': 'Set to not Download Media from Messages',
                    'default': False, 'required': False
                    },
                'group_id': {
                    'param': '--group_id', 'type': str, 'action': 'store',
                    'help': 'Target Group IDs. Ex: --group GroupA,GroupB,"Group C"',
                    'default': '*', 'required': False
                    },
                }
            },
        'list_groups': {
            'help': 'List all Downloaded Groups',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                }
            },
        'report': {
            'help': 'Generate the Report with all Messages and Medias',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
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
                'suppress_repeating_messages': {
                    'param': '--suppress_repeating_messages', 'type': str, 'action': 'store_true',
                    'help': 'Set the Date/Time Order to Descending',
                    'default': False, 'required': False
                    },
                }
            },
        'export_text': {
            'help': 'Export all Messages using Regex Filters',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'order_desc': {
                    'param': '--order_desc', 'type': str, 'action': 'store_true',
                    'help': 'Set the Date/Time Order to Descending',
                    'default': False, 'required': False
                    },
                'regex': {
                    'param': '--regex', 'type': str, 'action': 'store',
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
                'group_id': {
                    'param': '--group_id', 'type': str, 'action': 'store',
                    'help': 'Target Group IDs. Ex: --group GroupA,GroupB,"Group C"',
                    'default': '*', 'required': False
                    },
                }
            },
        'export_file': {
            'help': 'Export all Files by Mime Type',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'mime_type': {
                    'param': '--mime_type', 'type': str, 'action': 'store',
                    'help': 'Mimetype to be Exported',
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
                'group_id': {
                    'param': '--group_id', 'type': str, 'action': 'store',
                    'help': 'Target Group IDs. Ex: --group GroupA,GroupB,"Group C"',
                    'default': '*', 'required': False
                    },
                'filter': {
                    'param': '--filter', 'type': str, 'action': 'store',
                    'help': 'Filter by File Name parts. Ex: --filter my_apk,"My APK 2"',
                    'default': '*', 'required': False
                    }
                }
            },
        'sent_report_telegram': {
            'help': 'Sent the Current Report to a Telegram User using the Username',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'destination_username': {
                    'param': '--destination_username', 'type': str, 'action': 'store', 'help': 'Telegram Account Username',
                    'default': None, 'required': True
                    },
                'report_folder': {
                    'param': '--report_folder', 'type': str, 'action': 'store',
                    'help': 'Set the Report Output Folder',
                    'default': 'reports', 'required': False
                    },
                'title': {
                    'param': '--title', 'type': str, 'action': 'store',
                    'help': 'Report Title',
                    'default': 'TEx Report @@now@@', 'required': True
                    },
                'attachment_name': {
                    'param': '--attachment_name', 'type': str, 'action': 'store',
                    'help': 'Report Attachment FileName',
                    'default': 'report_@@now@@', 'required': True
                    },
                }
            },
        'stats': {
            'help': 'Show Stats from a Phone Number Groups, Messages, Assets',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'report_folder': {
                    'param': '--report_folder', 'type': str, 'action': 'store',
                    'help': 'Set the Report Output Folder',
                    'default': 'reports', 'required': False
                    },
                'limit_days': {
                    'param': '--limit_days', 'type': int, 'action': 'store',
                    'help': 'Limit Statistics Period in Days',
                    'default': 3650, 'required': False
                    },
                }
            },
        'purge_old_data': {
            'help': 'Purge old Messages, Media, etc',
            'sub_args': {
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                'limit_days': {
                    'param': '--limit_days', 'type': int, 'action': 'store',
                    'help': 'Limit Media Age Period in Days',
                    'default': 365, 'required': False
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
                'config': {
                    'param': '--config', 'type': str, 'action': 'store', 'help': 'Configuration File.',
                    'default': None, 'required': True,
                    },
                }
            }
        }

    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """Execute Module."""
        parent_parser = argparse.ArgumentParser(description=f'TEx - Telegram Monitor - {open("../__version__.txt", "r", encoding="utf-8").read()}')  # pylint: disable=R1732
        sub_parser = parent_parser.add_subparsers(title='actions', dest='action')

        # Add Parameters to Arg Parser
        for arg in InputArgsHandler.__ARGS:  # pylint: disable=C0206
            spec: Dict = InputArgsHandler.__ARGS[arg]

            parser_sub_command = sub_parser.add_parser(arg, help=spec['help'])

            for sub_arg in spec['sub_args']:
                sub_arg_spec: Dict = spec['sub_args'][sub_arg]

                parser_sub_command.add_argument(
                    sub_arg_spec['param'], action=sub_arg_spec['action'], dest=sub_arg,
                    help=sub_arg_spec['help'], default=sub_arg_spec['default'], required=sub_arg_spec['required']
                    )

        # Parse Args
        input_args: argparse.Namespace = parent_parser.parse_args()

        # Add to Result Args
        for arg in InputArgsHandler.__ARGS:  # pylint: disable=C0206

            args.update(
                {arg: getattr(input_args, 'action') == arg}  # noqa: B009
                )

            if args[arg]:  # Parse Only If the Action was True
                for sub_arg in InputArgsHandler.__ARGS[arg]['sub_args']:
                    sub_args: List[Dict] = await self._handle_sub_arg(input_args, sub_arg)
                    _ = [args.update(sub_arg) for sub_arg in sub_args]

        # Print Settings
        for key, value in args.items():
            logger.info(f'\t\t{key} = {value}')

    async def _handle_sub_arg(self, input_args: argparse.Namespace, sub_arg: str) -> List[Dict]:
        """Handle SubArgs."""
        if sub_arg == 'limit_days':
            return [
                {sub_arg: getattr(input_args, sub_arg)},
                {'start_at': ''},
                {'end_at': ''}
                ]

        return [{sub_arg: getattr(input_args, sub_arg)}]
