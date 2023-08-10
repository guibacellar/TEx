"""HTTP Navigation Manager."""

from typing import Dict, Optional

import requests


class HttpNavigationManager:
    """Http Navigation Manager."""

    __INSTANCE: Optional[requests.Session] = None

    @staticmethod
    def init(data: Dict) -> None:
        """Initialize Navigation Manager."""
        HttpNavigationManager.__INSTANCE = requests.Session()
        HttpNavigationManager.__INSTANCE.headers.update(
            {'User-Agent': data['web_navigation']['user_agent']}
            )

    @staticmethod
    def get(uri: str) -> str:
        """Realize a GET on Remote URI.

        :param uri: Target URI
        :return:
        """
        if not HttpNavigationManager.__INSTANCE:
            raise Exception("HttpNavigationManager not Initialized.")  # pylint: disable=W0719

        return HttpNavigationManager.__INSTANCE.get(uri).text

    @staticmethod
    def download_file(uri: str, target_path: str) -> None:
        """Download a Single File from Web.

        :param uri: Source File.
        :param target_path: Target File.
        :return:
        """
        if not HttpNavigationManager.__INSTANCE:
            raise Exception("HttpNavigationManager not Initialized.")  # pylint: disable=W0719

        with open(target_path, 'wb') as file:
            file.write(
                HttpNavigationManager.__INSTANCE.get(uri).content
                )

            file.flush()
            file.close()
