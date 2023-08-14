# TEx - **T**elegram **E**xplorer

[![](https://img.shields.io/github/last-commit/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/github/languages/code-size/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/maintainer-Th3%200bservator-blue)](https://theobservator.net/)
[![](https://github.com/guibacellar/TEx/actions/workflows/cy.yml/badge.svg?branch=main)](https://github.com/guibacellar/TEx/actions/workflows/cy.yml)

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#available-modules">Available Modules</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#command-line">Command Line</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

TEx is a Telegram Explorer tool created to help Researchers, Investigators and Law Enforcement Agents to Collect and Process the Huge Amount of Data Generated from Criminal, Fraud, Security and Others Telegram Groups.

  the available functionalities.


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

 * Python 3.8+

### Installation
pip install TEx

### Configuration
TEx need on at least, one configuration file. On reality, TEx need one configuration file for each *phone number* you want to use.

```editorconfig
[CONFIGURATION]
api_id=my_api_id
api_hash=my_api_hash
phone_number=my_phone_number
data_path=my_data_path
```

* **api_id** > Required - Telegram API ID. From https://my.telegram.org/ > login > API development tools 
* **api_hash** > Required - Telegram API Hash. From https://my.telegram.org/ > login > API development tools
* **phone_number** > Required - Target Phone Number
* **data_path** > Optional - Defines the Path Folder for the SQLite Databases and Dowloaded Files

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
TEx connect --config /usr/my_TEx_config.config
TEx load_groups --config /usr/my_TEx_config.config
TEx listen --config /usr/my_TEx_config.config
```

<!-- Command Line -->
## Command Line

### Connect to Telegram Servers
```bash
TEx connect --config CONFIGURATION_FILE_PATH
```
  * **config** > Required - Created Configuration File Path

### Update Groups List (Optional, but Recommended)
```bash
TEx load_groups --config CONFIGURATION_FILE_PATH --refresh_profile_photos
```

  * **config** > Required - Created Configuration File Path
  * **refresh_profile_photos** > Optional - If present, forces the Download and Update all Channels Members Profile Photo

### List Groups
```bash
TEx list_groups --config CONFIGURATION_FILE_PATH 
```

  * **config** > Required - Created Configuration File Path

### Listen Messages (Start the Message Listener)
```bash
TEx listen --config CONFIGURATION_FILE_PATH --group_id 1234,5678
```

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's

### Download Messages (Download since first message for each group)
```bash
TEx download_messages --config CONFIGURATION_FILE_PATH --group_id 1234,5678
```

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's

### Generate Report
```bash
TEx report --config CONFIGURATION_FILE_PATH --report_folder REPORT_FOLDER_PATH --group_id * --around_messages NUM --order_desc --limit_days 3 --filter FILTER_EXPRESSION_1,FILTER_EXPRESSION_2,FILTER_EXPRESSION_N
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
```bash
TEx export_file --config CONFIGURATION_FILE_PATH -report_folder REPORT_FOLDER_PATH --group_id * --filter * --limit_days 3 --mime_type text/plain
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **filter** > Optional - Simple (Comma Separated) FileName String Terms Filter. Ex: malware, "Bot net"
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **mime_type** > Optional - File MIME Type. Ex: application/vnd.android.package-archive


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
