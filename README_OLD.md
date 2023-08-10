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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

TEx is a Telegram Explorer tool created to help Researchers, Investigators and Law Enforcement Agents to Collect and Process the Huge Amount of Data Generated from Criminal, Fraud, Security and Others Telegram Groups.

Created in Python and using a Modular Architecture, the TEx easily allows to add new modules to enrich the available functionalities.


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

 * Python 3.8+

### Installation
pip install TeX

<!-- USAGE EXAMPLES -->
## Usage

There's 1 initial step to use and that is to connect to telegram.

### Command Line
#### Connect to Telegram Servers
```bash
python3 -m TEx connect --api_id TELEGRAM_API_ID --api_hash TELEGRAM_API_HASH --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH
```
  * **api_id** > Required - Telegram API ID. From https://my.telegram.org/ > login > API development tools 
  * **api_hash** > Required - Telegram API Hash. From https://my.telegram.org/ > login > API development tools
  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases

#### Update Groups List
```bash
python3 -m TEx load_groups --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH --refresh_profile_photos
```

  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases
  * **refresh_profile_photos** > Optional - If present, forces the Download and Update all Channels Members Profile Photo

#### List Groups
```bash
python3 -m TEx list_groups --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH
```

  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases

#### Download Message
```bash
python3 -m TEx download_messages --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH --group_id 1234,5678
```

  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's


#### Generate Report
```bash
python3 -m TEx report --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH --report_folder REPORT_FOLDER_PATH --group_id * --around_messages NUM --order_desc --limit_days 3 --filter FILTER_EXPRESSION_1,FILTER_EXPRESSION_2,FILTER_EXPRESSION_N
```
  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **around_messages** > Optional - Number of messages around (Before and After) the Filtered Message
  * **order_desc** > Optional - If present, sort all messages descending. Otherwise, sort Ascending.
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **filter** > Optional - Simple (Comma Separated) String Terms Filter. Ex: hacking,"Car Hacking",foo
  * **suppress_repeating_messages** > Optional - If present, suppress all repeating messages in the same report

#### Sent Report to Telegram User
TBD

#### Get Statistics
TBD

#### Export Text
TBD

#### Export Files
TBD

#### Maintenance - Purge Old Data
TBD

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/guibacellar/TEx/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


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
