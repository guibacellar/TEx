# Listen Messages

The Message Listener are the core of Telegram Explorer. This command starts a process to listen all messages provided by Telegram servers.

> The Message Listener performs an Automatically Groups and Users Synchronization.

Once started, the Telegram Explorer runner do not stops or terminate until the Telegram servers disconnect the client, or, the running process receives a SIGTERM to stop the process.

**Full Command:**

```bash
python3 -m TEx listen --config CONFIGURATION_FILE_PATH --ignore_media --group_id 1234,5678
```

**Basic Command:**
```bash
python3 -m TEx listen --config CONFIGURATION_FILE_PATH
```

**Parameters**

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's. Comma Separated


> ⚠️ **IMPORTANT**⚠️ </br></br> Currently, the maximum download size allowed on TeX are 256 MB. Any media larger that size do not be downloaded.

*Output Example:*
```bash
TEx - Telegram Explorer
Version 0.2.12
By: Th3 0bservator

2023-10-01 20:46:53,880 - INFO - [*] Loading Configurations:
2023-10-01 20:46:53,880 - INFO - [*] Installed Modules:
2023-10-01 20:46:53,880 - INFO - 	data_structure_handler.py
2023-10-01 20:46:53,880 - INFO - 	database_handler.py
2023-10-01 20:46:53,880 - INFO - 	execution_configuration_handler.py
2023-10-01 20:46:53,880 - INFO - 	telegram_connection_manager.py
2023-10-01 20:46:53,880 - INFO - 	telegram_groups_list.py
2023-10-01 20:46:53,880 - INFO - 	telegram_groups_scrapper.py
2023-10-01 20:46:53,880 - INFO - 	telegram_maintenance
2023-10-01 20:46:53,880 - INFO - 	telegram_messages_listener.py
2023-10-01 20:46:53,880 - INFO - 	telegram_messages_scrapper.py
2023-10-01 20:46:53,881 - INFO - 	telegram_report_generator
2023-10-01 20:46:53,881 - INFO - 	telegram_stats_generator.py
2023-10-01 20:46:53,891 - INFO - [*] Loading Execution Configurations:
2023-10-01 20:46:54,179 - INFO - [*] Executing Pipeline:
2023-10-01 20:46:54,179 - INFO - 	[+] telegram_connection_manager.TelegramConnector
2023-10-01 20:46:55,763 - INFO - 		User Authorized on Telegram: True
2023-10-01 20:46:55,775 - INFO - 	[+] telegram_messages_listener.TelegramGroupMessageListener
2023-10-01 20:46:55,912 - INFO - 		Listening Past Messages...
2023-10-01 20:46:55,912 - INFO - 		Listening New Messages...
2023-10-01 20:46:55,923 - INFO - 			Downloading Photo from Message 20436 at 2023-09-30 00:58:35
2023-10-01 20:46:56,774 - INFO - 			Downloading Photo from Message 788 at 2023-09-30 09:48:51
2023-10-01 20:46:56,805 - INFO - 			Downloading Photo from Message 20438 at 2023-09-30 11:18:12
2023-10-01 20:46:56,807 - INFO - 			Downloading Photo from Message 37345 at 2023-09-30 04:39:54
2023-10-01 20:46:56,823 - INFO - 			Downloading Photo from Message 37346 at 2023-09-30 13:12:39
2023-10-01 20:46:58,053 - INFO - 			Downloading Photo from Message 725 at 2023-09-30 15:07:38
2023-10-01 20:46:58,105 - INFO - 			Downloading Photo from Message 727 at 2023-09-30 15:16:05
2023-10-01 20:46:58,148 - INFO - 			Downloading Photo from Message 20440 at 2023-09-30 14:52:21
2023-10-01 20:46:58,149 - INFO - 			Downloading Photo from Message 37347 at 2023-09-30 15:23:33
2023-10-01 20:46:58,743 - WARNING - 		Group "1246578969" not found on DB. Performing automatic synchronization. Consider execute "load_groups" command to perform a full group synchronization (Members and Group Cover Photo).
2023-10-01 20:46:58,751 - INFO - 			Downloading Photo from Message 13855 at 2023-09-30 21:00:09
2023-10-01 20:46:58,752 - INFO - 			Downloading Media from Message 12587 (9739.13 Kbytes) as video/mp4 at 2023-09-30 21:37:30
2023-10-01 20:46:58,779 - INFO - 			Downloading Photo from Message 37348 at 2023-09-30 22:10:03
2023-10-01 20:46:59,062 - WARNING - 		User "1254788963" was not found on DB. Performing automatic synchronization.
2023-10-01 20:46:59,110 - INFO - 			Downloading Photo from Message 13856 at 2023-10-01 02:08:19
2023-10-01 20:46:59,111 - INFO - 			Downloading Photo from Message 13857 at 2023-10-01 02:08:19
```