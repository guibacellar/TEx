# TEx - **T**elegram **E**xplorer

![](https://img.shields.io/github/last-conao cmmit/guibacellar/TEx)
![](https://img.shields.io/github/languages/code-size/guibacellar/TEx)
![](https://img.shields.io/badge/Python-3.8+-green.svg)
![](https://img.shields.io/badge/maintainer-Th3%200bservator-blue)

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
TBD

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

#### Download Message
```bash
python3 -m TEx download_messages --phone_number TARGET_PHONE_NUMBER --data_path DATA_FOLDER_PATH
```

  * **phone_number** > Required - Target Phone Number
  * **data_path** > Optional - Defines the Path Folder for the SQLite Databases
  * **ignore_media** > Optional - If present, don't Download any Media

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
