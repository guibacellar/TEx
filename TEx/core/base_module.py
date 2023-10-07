"""OSIx Base Module."""
from __future__ import annotations

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

    @abc.abstractmethod
    async def can_activate(self, config: ConfigParser, args: Dict, data: Dict) -> bool:
        """
        Abstract Method for Module Activation Function.

        :return:
        """
