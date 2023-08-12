# """Telegram Maintenance - Purge old Data Manager Tests."""
#
# import asyncio
# import unittest
# from configparser import ConfigParser
# from typing import Dict
# import datetime
#
# import pytz
# from sqlalchemy import delete
#
# from TEx.core.dir_manager import DirectoryManagerUtils
# from TEx.database.db_initializer import DbInitializer
# from TEx.database.db_manager import DbManager
# from TEx.database.telegram_group_database import TelegramGroupDatabaseManager, TelegramMessageDatabaseManager
# from TEx.models.database.telegram_db_model import (
#     TelegramGroupOrmEntity,
#     TelegramMediaOrmEntity, TelegramMessageOrmEntity
# )
# from TEx.modules.telegram_groups_list import TelegramGroupList
# from TEx.modules.telegram_groups_scrapper import TelegramGroupScrapper
# from TEx.modules.telegram_maintenance.telegram_purge_old_data import TelegramMaintenancePurgeOldData
#
#
# class TelegramMaintenancePurgeOldDataTest(unittest.TestCase):
#
#     def setUp(self) -> None:
#
#         self.config = ConfigParser()
#         self.config.read('../../config.ini')
#
#         DirectoryManagerUtils.ensure_dir_struct('_data')
#         DirectoryManagerUtils.ensure_dir_struct('_data/resources')
#
#         DbInitializer.init(data_path='_data/', args={})
#         DbManager.SESSIONS['data'].execute(delete(TelegramGroupOrmEntity))
#         DbManager.SESSIONS['data'].execute(delete(TelegramMessageOrmEntity))
#         DbManager.SESSIONS['data'].commit()
#
#         # Add Group 1 - Without Any Message
#         TelegramGroupDatabaseManager.insert_or_update({
#             'id': 1, 'constructor_id': 'A', 'access_hash': 'AAAAAA',
#             'fake': False, 'gigagroup': False, 'has_geo': False,
#             'participants_count': 1, 'restricted': False,
#             'scam': False, 'group_username': 'UN-A',
#             'verified': False, 'title': 'UT-01', 'source': 'MyTestPhoneNumber5'
#         })
#
#         # Add Group 2 - With Previous Messages
#         TelegramGroupDatabaseManager.insert_or_update({
#             'id': 2, 'constructor_id': 'B', 'access_hash': 'BBBBBB',
#             'fake': False, 'gigagroup': False, 'has_geo': False,
#             'participants_count': 2, 'restricted': False,
#             'scam': False, 'group_username': 'UN-b',
#             'verified': False, 'title': 'UT-02', 'source': 'MyTestPhoneNumber5'
#         })
#
#         # Add Messages from Past Date - Group 1
#         TelegramMessageDatabaseManager.insert({
#             'id': 11, 'group_id': 1, 'date_time': datetime.datetime.now(tz=pytz.utc),
#             'message': 'Message 11', 'raw': 'Raw Message 1', 'from_id': None, 'from_type': None,
#             'to_id': None, 'media_id': None
#         })
#
#         TelegramMessageDatabaseManager.insert({
#             'id': 12, 'group_id': 1, 'date_time': datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=1),
#             'message': 'Message 12', 'raw': 'Raw Message 2', 'from_id': None, 'from_type': None,
#             'to_id': None, 'media_id': None
#         })
#
#       # Add Messages from Past Date - Group 2
#         TelegramMessageDatabaseManager.insert({
#             'id': 21, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc),
#             'message': 'Message 21', 'raw': 'Raw Message 12', 'from_id': None, 'from_type': None,
#             'to_id': None, 'media_id': None
#         })
#
#         TelegramMessageDatabaseManager.insert({
#             'id': 22, 'group_id': 2, 'date_time': datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(days=2),
#             'message': 'Message 22', 'raw': 'Raw Message 22', 'from_id': None, 'from_type': None,
#             'to_id': None, 'media_id': None
#         })
#
#         # Initialize the Medias Groups
#         DbInitializer.init_media_dbs(data_path='_data/', args={'target_phone_number': 'MyTestPhoneNumber5'})
#
#         # Cleanup Media DBs
#         DbManager.SESSIONS['media_1'].execute(delete(TelegramMediaOrmEntity))
#         DbManager.SESSIONS['media_2'].execute(delete(TelegramMediaOrmEntity))
#         DbManager.SESSIONS['data'].commit()
#
#     def tearDown(self) -> None:
#         DbManager.SESSIONS['media_1'].close()
#         DbManager.SESSIONS['media_2'].close()
#         DbManager.SESSIONS['data'].close()
#
#     def test_run(self):
#         """Test Run Method."""
#
#         target: TelegramGroupScrapper = TelegramMaintenancePurgeOldData()
#         args: Dict = {
#             'purge_old_data': True,
#             'target_phone_number': 'MyTestPhoneNumber5',
#             'limit_days': 1
#         }
#         data: Dict = {}
#
#         with self.assertLogs() as captured:
#             loop = asyncio.get_event_loop()
#             loop.run_until_complete(
#                 target.run(
#                     config=self.config,
#                     args=args,
#                     data=data
#                 )
#             )
#
#             # Check Logs
#             self.assertEqual(4, len(captured.records))
#             # self.assertEqual('		Found 2 Groups', captured.records[0].message)
#             # self.assertEqual('		ID       	Username	Title', captured.records[1].message)
#             # self.assertEqual('		1	UN-A	UT-01', captured.records[2].message)
#             # self.assertEqual('		2	UN-b	UT-02', captured.records[3].message)
