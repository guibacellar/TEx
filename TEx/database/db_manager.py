"""Database Manager."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DbManager:

    SQLALCHEMY_BINDS = {}
    SESSIONS = {}

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

    @staticmethod
    def init_media_db(group_id: str, data_path: str) -> None:
        """Initialize All Media DataBases."""

        DbManager.SQLALCHEMY_BINDS[f'media_{group_id}'] = create_engine(
            f'sqlite:///{os.path.join(data_path, "media", f"media_{group_id}.db")}',
            connect_args={"check_same_thread": False},
            echo=False, logging_name='sqlalchemy', isolation_level='READ UNCOMMITTED'
        )

        DbManager.SESSIONS[f'media_{group_id}'] = sessionmaker(autocommit=False, autoflush=False, bind=DbManager.SQLALCHEMY_BINDS[f'media_{group_id}'])()