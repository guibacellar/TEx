"""Directory Manager."""

import os


class DirectoryManagerUtils:
    """Directory Manager."""

    @staticmethod
    def ensure_dir_struct(path: str) -> None:
        """Ensure That Directory Exists.

        :param path:
        :return:
        """
        target_path: str = os.path.abspath(os.path.join(os.getcwd(), path))

        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
