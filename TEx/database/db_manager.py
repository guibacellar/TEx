"""Database Manager."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class DbManager:

    SQLALCHEMY_BINDS = {}
    temp_session: Session = None
    data_session: Session = None

    @staticmethod
    def init_db(data_path: str) -> None:
        """Initialize the DB COnnection."""

        DbManager.SQLALCHEMY_BINDS = {
            'temp': create_engine(
                f'sqlite:///{os.path.join(data_path, "temp_local.db")}',
                connect_args={"check_same_thread": False},
                echo=False, logging_name='sqlalchemy'
            ),
            'data': create_engine(
                f'sqlite:///{os.path.join(data_path, "data_local.db")}',
                connect_args={"check_same_thread": False},
                echo=False, logging_name='sqlalchemy'
            )
        }

        DbManager.temp_session = sessionmaker(autocommit=False, autoflush=False, bind=DbManager.SQLALCHEMY_BINDS['temp'])()
        DbManager.data_session = sessionmaker(autocommit=False, autoflush=False, bind=DbManager.SQLALCHEMY_BINDS['data'])()

