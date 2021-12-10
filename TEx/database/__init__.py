# """Database Module."""
#
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session, sessionmaker
#
# class DbControl:
#
#     SQLALCHEMY_BINDS = {}
#
#     temp_session: Session = None
#     data_session: Session = None
#
#     def init_db(data_path: str) -> None:
#         """Initialize the DB COnnection."""
#
#         SQLALCHEMY_BINDS = {
#             'temp': create_engine(
#                 f'sqlite:///{os.path.join(data_path, "temp_local.db")}',
#                 connect_args={"check_same_thread": False},
#                 echo=False, logging_name='sqlalchemy'
#             ),
#             'data': create_engine(
#                 f'sqlite:///{os.path.join(data_path, "data_local.db")}',
#                 connect_args={"check_same_thread": False},
#                 echo=False, logging_name='sqlalchemy'
#             )
#         }
#
#         temp_session = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_BINDS['temp'])()
#         data_session  = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_BINDS['data'])()
#
