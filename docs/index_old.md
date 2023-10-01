# Welcome to Telegram Explorer


[![](https://img.shields.io/github/last-commit/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/github/languages/code-size/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/maintainer-Th3%200bservator-blue)](https://theobservator.net/)
[![](https://github.com/guibacellar/TEx/actions/workflows/cy.yml/badge.svg?branch=main)](https://github.com/guibacellar/TEx/actions/workflows/cy.yml)
[![](https://telegramexplorer.readthedocs.io/en/latest/?badge=latest)](https://telegramexplorer.readthedocs.io/en/latest/)

<!-- USAGE EXAMPLES -->
## Usage
Basic TEx Usage.

Considering a *my_TEx_config.config* file created at */usr/my_TEx_config.config* with follow:

```editorconfig
[CONFIGURATION]
api_id=12345678
api_hash=dff159855418ddfaddf10dcbdeadbeef
phone_number=5511987654321
data_path=/usr/TEx/
```

Execute the first 2 commands to configure and sync TEx and the last one to activate the listener module.

```bash
python3 -m TEx connect --config /usr/my_TEx_config.config
python3 -m TEx load_groups --config /usr/my_TEx_config.config
python3 -m TEx listen --config /usr/my_TEx_config.config
```

<!-- Command Line -->
## Command Line

### Connect to Telegram Servers
```bash
python3 -m TEx connect --config CONFIGURATION_FILE_PATH
```
  * **config** > Required - Created Configuration File Path

### Update Groups List (Optional, but Recommended)
```bash
python3 -m TEx load_groups --config CONFIGURATION_FILE_PATH --refresh_profile_photos
```

  * **config** > Required - Created Configuration File Path
  * **refresh_profile_photos** > Optional - If present, forces the Download and Update all Channels Members Profile Photo

### List Groups
```bash
python3 -m TEx list_groups --config CONFIGURATION_FILE_PATH 
```

  * **config** > Required - Created Configuration File Path

### Listen Messages (Start the Message Listener)
```bash
python3 -m TEx listen --config CONFIGURATION_FILE_PATH --group_id 1234,5678
```

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's

### Download Messages (Download since first message for each group)
Scrap Messages from Telegram Server
```bash
python3 -m TEx download_messages --config CONFIGURATION_FILE_PATH --group_id 1234,5678
```

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's

### Generate Report
Generate HTML Report
```bash
python3 -m TEx report --config CONFIGURATION_FILE_PATH --report_folder REPORT_FOLDER_PATH --group_id * --around_messages NUM --order_desc --limit_days 3 --filter FILTER_EXPRESSION_1,FILTER_EXPRESSION_2,FILTER_EXPRESSION_N
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **around_messages** > Optional - Number of messages around (Before and After) the Filtered Message
  * **order_desc** > Optional - If present, sort all messages descending. Otherwise, sort Ascending.
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **filter** > Optional - Simple (Comma Separated) String Terms Filter. Ex: hacking,"Car Hacking",foo
  * **suppress_repeating_messages** > Optional - If present, suppress all repeating messages in the same report

### Export Downloaded Files
Export Downloaded Files by MimeType
```bash
python3 -m TEx export_file --config CONFIGURATION_FILE_PATH -report_folder REPORT_FOLDER_PATH --group_id * --filter * --limit_days 3 --mime_type text/plain
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **filter** > Optional - Simple (Comma Separated) FileName String Terms Filter. Ex: malware, "Bot net"
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **mime_type** > Optional - File MIME Type. Ex: application/vnd.android.package-archive

### Export Texts
Export Messages (Texts) using Regex finder
```bash
python3 -m TEx export_text --config CONFIGURATION_FILE_PATH --order_desc --limit_days 3 --regex REGEX --report_folder REPORT_FOLDER_PATH --group_id *
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **regex** > Required - Regex to find the messages. 
    * Ex: Export Links from Messages (.*http://.*),(.*https://.*)

<!-- LICENSE -->
## License

Distributed under the Apache License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

**Th3 0bservator**

[![Foo](https://img.shields.io/badge/RSS-FFA500?style=for-the-badge&logo=rss&logoColor=white)](https://www.theobservator.net/) 
[![Foo](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/th3_0bservator) 
[![Foo](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guibacellar/) 
[![Foo](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/guilherme-bacellar/)
