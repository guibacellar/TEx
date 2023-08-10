"""Database Manager."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbManager:
    """Main Database Manager."""

    SQLALCHEMY_BINDS = {}  # type:ignore
    SESSIONS = {}  # type:ignore

    @staticmethod
    def init_db(data_path: str) -> None:
        """Initialize the DB Connection."""
        DbManager.SQLALCHEMY_BINDS = {
            'temp': create_engine(
                f'sqlite:///{os.path.join(data_path, "temp_local.db")}',
                connect_args={"check_same_thread": False},
                echo=False, logging_name='sqlalchemy', isolation_level='READ UNCOMMITTED'
                ),
            'data': create_engine(
                f'sqlite:///{os.path.join(data_path, "data_local.db")}',
                connect_args={"check_same_thread": False},
                echo=False, logging_name='sqlalchemy', isolation_level='READ UNCOMMITTED'
                )
            }

        DbManager.SESSIONS = {
            'temp': sessionmaker(autocommit=False, autoflush=False, bind=DbManager.SQLALCHEMY_BINDS['temp'])(),
            'data': sessionmaker(autocommit=False, autoflush=False, bind=DbManager.SQLALCHEMY_BINDS['data'])()
            }
