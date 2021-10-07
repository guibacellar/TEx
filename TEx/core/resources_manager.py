"""Resources File Handle."""

import os
from typing import List


class ResourcesFileHandler:
    """Resources File Hander."""

    @staticmethod
    def file_exist(path: str) -> bool:
        """
        Return if a File Exists.

        :param path: File Path
        :return:
        """
        return os.path.exists(os.path.join('resources', path))

    @staticmethod
    def read_file_text(path: str) -> List[str]:
        """Read All File Content.

        :param path: File Path
        :return: File Content
        """
        with open(os.path.join(os.getcwd(), 'resources', path), 'r', encoding='utf-8') as file:
            return file.readlines()
