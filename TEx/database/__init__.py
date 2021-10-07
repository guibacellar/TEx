"""Database Module."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_BINDS = {
    'temp': create_engine(
        f'sqlite:///{os.path.join(os.getcwd(), "data", "temp_local.db")}',
        connect_args={"check_same_thread": False},
        echo=False, logging_name='sqlalchemy'
        ),
    'data': create_engine(
        f'sqlite:///{os.path.join(os.getcwd(), "data", "data_local.db")}',
        connect_args={"check_same_thread": False},
        echo=False, logging_name='sqlalchemy'
        )
    }

temp_session: Session = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_BINDS['temp'])()
data_session: Session = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_BINDS['data'])()
