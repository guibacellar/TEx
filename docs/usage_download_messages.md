# Download Messages (Download since first message for each group)

Unlike the process of listening to messages, this command downloads messages from Telegram groups from the first message. Essentially downloading every message, every media (if 'ignore_media' was not present).

We can compare this command with any scrapper.

> 🚨🚨🚨🚨🚨 **CRITICAL INFORMATION**🚨🚨🚨🚨🚨 </br></br> Download all messages from all groups can lead your account to be banned. So, use carefully only and if necessary.</br></br>**Note:** Extremely recommended to use with the groups filter.

**Full Command:**
```bash
python3 -m TEx download_messages --config CONFIGURATION_FILE_PATH --ignore_media --group_id 1234,5678
```

**Basic Command:**
```bash
python3 -m TEx download_messages --config CONFIGURATION_FILE_PATH
```

**Parameters**

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's


*Output Example:*
```bash
2023-10-01 21:01:35,543 - INFO - [*] Loading Configurations:
2023-10-01 21:01:35,543 - INFO - [*] Installed Modules:
2023-10-01 21:01:35,543 - INFO - 	data_structure_handler.py
2023-10-01 21:01:35,543 - INFO - 	database_handler.py
2023-10-01 21:01:35,543 - INFO - 	execution_configuration_handler.py
2023-10-01 21:01:35,543 - INFO - 	telegram_connection_manager.py
2023-10-01 21:01:35,544 - INFO - 	telegram_groups_list.py
2023-10-01 21:01:35,544 - INFO - 	telegram_groups_scrapper.py
2023-10-01 21:01:35,544 - INFO - 	telegram_maintenance
2023-10-01 21:01:35,544 - INFO - 	telegram_messages_listener.py
2023-10-01 21:01:35,544 - INFO - 	telegram_messages_scrapper.py
2023-10-01 21:01:35,544 - INFO - 	telegram_report_generator
2023-10-01 21:01:35,544 - INFO - 	telegram_stats_generator.py
2023-10-01 21:01:35,894 - INFO - [*] Executing Pipeline:
2023-10-01 21:01:42,659 - INFO - 	[+] telegram_messages_scrapper.TelegramGroupMessageScrapper
2023-10-01 21:01:42,706 - INFO - 		Found 2 Groups
2023-10-01 21:01:43,468 - INFO - 		Download Messages from "My Group 1" > Last Offset: 3936
2023-10-01 21:01:54,468 - INFO - 		Download Messages from "TeX Beta Group" > Last Offset: 158742
2023-10-01 20:37:27,859 - INFO - [*] Executing Termination:
2023-10-01 20:07:27,958 - INFO - 	[+] state_file_handler.SaveStateFileHandler
```