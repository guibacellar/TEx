# List Groups

You can list groups directly in the console/tty output for a quick view of all groups already present in the database.

**Full Command:**

```bash
python3 -m TEx list_groups --config CONFIGURATION_FILE_PATH 
```

**Parameters**

  * **config** > Required - Created Configuration File Path

*Output Example:*
```bash
TEx - Telegram Explorer
Version 0.2.12
By: Th3 0bservator

2023-10-01 20:41:15,142 - INFO - [*] Loading Configurations:
2023-10-01 20:41:15,142 - INFO - [*] Installed Modules:
2023-10-01 20:41:15,143 - INFO - 	data_structure_handler.py
2023-10-01 20:41:15,143 - INFO - 	database_handler.py
2023-10-01 20:41:15,143 - INFO - 	execution_configuration_handler.py
2023-10-01 20:41:15,143 - INFO - 	telegram_connection_manager.py
2023-10-01 20:41:15,143 - INFO - 	telegram_groups_list.py
2023-10-01 20:41:15,143 - INFO - 	telegram_groups_scrapper.py
2023-10-01 20:41:15,143 - INFO - 	telegram_maintenance
2023-10-01 20:41:15,143 - INFO - 	telegram_messages_listener.py
2023-10-01 20:41:15,143 - INFO - 	telegram_messages_scrapper.py
2023-10-01 20:41:15,143 - INFO - 	telegram_report_generator
2023-10-01 20:41:15,143 - INFO - 	telegram_stats_generator.py
2023-10-01 20:41:15,484 - INFO - [*] Executing Pipeline:
2023-10-01 20:41:15,823 - INFO - 	[+] telegram_groups_list.TelegramGroupList
2023-10-01 20:41:16,535 - INFO - 		Found 2 Groups
2023-10-01 20:41:16,536 - INFO - 		ID       	Username                     	Title                                                                                  
2023-10-01 20:41:16,536 - INFO - 		1769587896	mygroup1                    	My Group 1                                                                        
2023-10-01 20:41:16,536 - INFO - 		1259876541	texbetagroup                   	TeX Beta Group                                                                       
2023-10-01 20:41:16,703 - INFO - [*] Executing Termination:
2023-10-01 20:41:16,703 - INFO - 	[+] state_file_handler.SaveStateFileHandler
```