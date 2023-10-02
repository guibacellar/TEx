# Update Groups List

Despite the fact that the Telegram Explorer performs automatic group synchronization every time when a new group/chat is detected, the automatic system only register the group inside database.

The Group Load command perform a full group synchronization, including all information about te group (name, pictures and full members list, members photos, etc).

**Full Command:**

```bash
python3 -m TEx load_groups --config CONFIGURATION_FILE_PATH --refresh_profile_photos
```

**Basic Command:**

```bash
python3 -m TEx load_groups --config CONFIGURATION_FILE_PATH
```

**Parameters**

  * **config** > Required - Created Configuration File Path
  * **refresh_profile_photos** > Optional - If present, forces the Download and Update all Channels Members Profile Photo

*Output Example:*
```bash
TEx - Telegram Explorer
Version 0.2.12
By: Th3 0bservator

2023-10-01 20:37:14,514 - INFO - [*] Loading Configurations:
2023-10-01 20:37:14,514 - INFO - [*] Installed Modules:
2023-10-01 20:37:14,514 - INFO - 	data_structure_handler.py
2023-10-01 20:37:14,514 - INFO - 	database_handler.py
2023-10-01 20:37:14,515 - INFO - 	execution_configuration_handler.py
2023-10-01 20:37:14,515 - INFO - 	telegram_connection_manager.py
2023-10-01 20:37:14,515 - INFO - 	telegram_groups_list.py
2023-10-01 20:37:14,515 - INFO - 	telegram_groups_scrapper.py
2023-10-01 20:37:14,515 - INFO - 	telegram_maintenance
2023-10-01 20:37:14,515 - INFO - 	telegram_messages_listener.py
2023-10-01 20:37:14,515 - INFO - 	telegram_messages_scrapper.py
2023-10-01 20:37:14,515 - INFO - 	telegram_report_generator
2023-10-01 20:37:14,515 - INFO - 	telegram_stats_generator.py
2023-10-01 20:37:14,525 - INFO - [*] Loading Execution Configurations:
2023-10-01 20:37:14,525 - INFO - 	[+] data_structure_handler.DataStructureHandler
2023-10-01 20:37:14,813 - INFO - [*] Executing Pipeline:
2023-10-01 20:37:21,361 - INFO - 	[+] telegram_groups_scrapper.TelegramGroupScrapper
2023-10-01 20:37:21,364 - INFO - 		Enumerating Groups
2023-10-01 20:37:22,169 - INFO - 		Processing "My Group 1 (1769587896)" Members and Group Profile Picture
2023-10-01 20:37:27,782 - INFO - 		Processing "TeX Beta Group (1259876541)" Members and Group Profile Picture
2023-10-01 20:37:27,859 - INFO - [*] Executing Termination:
2023-10-01 20:07:27,958 - INFO - 	[+] state_file_handler.SaveStateFileHandler
```