"""Database Manager."""

import os
from sqlite3 import Connection

from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import _ConnectionRecord


class DbManager:
    """Main Database Manager."""

    SQLALCHEMY_BINDS = {}  # type:ignore
    SESSIONS = {}  # type:ignore

    @staticmethod
    def init_db(data_path: str) -> None:
        """Initialize the DB Connection."""
        DbManager.SQLALCHEMY_BINDS = {
            'temp': create_engine(
                f'sqlite:///{os.path.join(data_path, "temp_local.db")}?nolock=1&check_same_thread=false',
                connect_args={'check_same_thread': False, 'timeout': 120},
                echo=False, logging_name='sqlalchemy',
                ),
            'data': create_engine(
                f'sqlite:///{os.path.join(data_path, "data_local.db")}?nolock=1&check_same_thread=false',
                connect_args={'check_same_thread': False, 'timeout': 120},
                echo=False, logging_name='sqlalchemy',
                ),
            }

        DbManager.SESSIONS = {
            'temp': sessionmaker(autocommit=False, autoflush=True, bind=DbManager.SQLALCHEMY_BINDS['temp'])(),
            'data': sessionmaker(autocommit=False, autoflush=True, bind=DbManager.SQLALCHEMY_BINDS['data'])(),
            }

        listen(DbManager.SQLALCHEMY_BINDS['data'], 'connect', DbManager.do_connect)

    @staticmethod
    def do_connect(dbapi_connection: Connection, connection_record: _ConnectionRecord) -> None:
        """Disable SQLLite Transaction auto Start."""
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None
