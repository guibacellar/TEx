"""OSIx Base Module."""

import abc
from configparser import ConfigParser
from typing import Dict


class BaseModule:
    """Base Module Declaration."""

    @abc.abstractmethod
    async def run(self, config: ConfigParser, args: Dict, data: Dict) -> None:
        """
        Abstract Base Run Description.

        :return: None
        """
