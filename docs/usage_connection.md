# Connection to Telegram Servers

First step for every phone number to be used is to connect to Telegram servers. After that, the runner will create a session file under *'data_path'* folder specified in the configuration file.

**Full Command:**

```bash
python3 -m TEx connect --config CONFIGURATION_FILE_PATH
```

**Parameters**

  * **config** > Required - Created Configuration File Path

*Output Example:*
```bash
TEx - Telegram Explorer
Version 0.2.12
By: Th3 0bservator

2023-10-01 20:07:06,501 - INFO - [*] Loading Configurations:
2023-10-01 20:07:06,502 - INFO - [*] Installed Modules:
2023-10-01 20:07:06,502 - INFO - 	data_structure_handler.py
2023-10-01 20:07:06,502 - INFO - 	database_handler.py
2023-10-01 20:07:06,502 - INFO - 	execution_configuration_handler.py
2023-10-01 20:07:06,502 - INFO - 	telegram_connection_manager.py
2023-10-01 20:07:06,502 - INFO - 	telegram_groups_list.py
2023-10-01 20:07:06,502 - INFO - 	telegram_groups_scrapper.py
2023-10-01 20:07:06,502 - INFO - 	telegram_maintenance
2023-10-01 20:07:06,502 - INFO - 	telegram_messages_listener.py
2023-10-01 20:07:06,502 - INFO - 	telegram_messages_scrapper.py
2023-10-01 20:07:06,502 - INFO - 	telegram_report_generator
2023-10-01 20:07:06,502 - INFO - 	telegram_stats_generator.py
2023-10-01 20:07:06,987 - INFO - [*] Executing Pipeline:
2023-10-01 20:07:06,987 - INFO - 	[+] telegram_connection_manager.TelegramConnector
2023-10-01 20:07:07,392 - INFO - 		Authorizing on Telegram...
2023-10-01 20:07:13,590 - INFO - 		User Authorized on Telegram: True
2023-10-01 20:07:13,851 - INFO - [*] Executing Termination:
2023-10-01 20:07:13,851 - INFO - 	[+] state_file_handler.SaveStateFileHandler
```