# OSIx - **O**pen **S**ource **I**ntelligence e**X**plorer

[![CI](https://github.com/guibacellar/OSIx/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/guibacellar/OSIx/actions/workflows/ci.yml)
![](https://img.shields.io/github/last-commit/guibacellar/OSIx)
![](https://img.shields.io/github/languages/code-size/guibacellar/OSIx)
![](https://img.shields.io/badge/Python-3.7.6+-green.svg)
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

OSIx is a OSINT (Open Source Intelligence) tool created to help Researchers, Investigators and Law Enforcement Agents to Collect and Process Open Data.

Created in Python and using a Modular Architecture, the OSIx easily allows to add new modules to enrich the available functionalities.


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

 * Python 3.6.7+

### Installation

**Stable**
```bash
pip3 install OSIx
```

**In Development**
```bash
pip3 install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple OSIx  
```

<!-- AVAILABLE MODULES -->
## Available Modules

* Username Search
  * [Username Searcher](docs/module_username.md) - Allow to find the Specified Username in 150+ Websites (Including NSFW Ones) and Export a CSV file with the Founded Entries;
    * GitHub Username Grabber - Download GitHub Data from Specified Username (Profile Data, Location, Repositories, Followers and Following Accounts);
    * Steam Username Grabber - Download Steam Data from Specified Username (Name, Location, SteamId's, Location and Profile Picture, Stats and Creation Date);
    * Pastebin Username Grabber - Download Steam Data from Specified Username (Username, Views Count, All Pastes Views Count, Profile Picture and all Public Pastes);
    * Gravatar Username Grabber - Download Gravatar Data from Specified Username (Username, FullName, Gravatar ID, Location, Profile Picture and Public Links);
* [Bitcoin Wallet Info & Transactions](docs/module_btc_wallet.md) - Download the Bitcoin Transactions from a Wallet and Generates Graphs for Visualization (Gephi and GraphML Compatible);


<!-- USAGE EXAMPLES -->
## Usage

### Command Line

```bash
usage: python3 -m OSIx [-h] [--job_name JOB_NAME] [--purge_temp_files]
               [--btc_wallet BTC_WALLET] [--btc_get_transactions]
               [--export_btc_transactions_as_graphml]
               [--export_btc_transactions_as_gephi] [--username USERNAME]
               [--username_scan] [--username_allow_nsfw_scan]
               [--username_print_result] [--username_show_all]
               [--username_enable_dump_file]

optional arguments:
  -h, --help            show this help message and exit
  --job_name JOB_NAME   Job Name. Used to Save/Restore State File.
  --purge_temp_files    Force Delete All Temporary Files
  --btc_wallet BTC_WALLET
                        BitCoin Wallet Address
  --btc_get_transactions
                        Allow to Download All BitCoin Transactions from Wallet
  --export_btc_transactions_as_graphml
                        Allow to Export the BitCoin Transactions as GraphML
  --export_btc_transactions_as_gephi
                        Allow to Export the BitCoin Transactions as Gephi File
  --username USERNAME   Username to Search
  --username_scan       Allow the Executor to Scan the the Username in All
                        Social Networks and WebSites
  --username_allow_nsfw_scan
                        Allow the Executor to Scan the NSFW WebSites
  --username_print_result
                        Allow to Print the Result in sysout
  --username_show_all   Allow to Print all Results, otherwise, Print Only the
                        Founded Ones.
  --username_enable_dump_file
                        Allow to Dump a Result file into data/export Folder.


```


**Jobname**

The *job_name* parameter allow to specify a job name to the executor and the executor will save a state file with all parameters and configurations.

```bash
python3 -m OSIx --job_name MY_JOB
```

**Purge All Temporary Files**

The *purge_temp_files* parameter tell's to the executor to cleanup all generated temporary files.

```bash
python3 -m OSIx --purge_temp_files
```

**Output Example**
```bash
python3 -m OSIx \
        --username marcos --username_allow_nsfw_scan \
        --username_print_result --username_enable_dump_file

[*] Loading Configurations:
[*] Installed Modules:
	bitcoin_wallet.py
	bitcoin_wallet_graph.py
	http_navigation_manager.py
	input_args_handler.py
	state_file_handler.py
	steam_username_data_digger.py
	temp_file_manager.py
	username_handler.py
[*] Executing Pipeline:
	[+] input_args_handler.InputArgsHandler
		job_name = dev_001
		purge_temp_files = False
		btc_wallet = 
		btc_get_transactions = 
		export_btc_transactions_as_graphml = False
		export_btc_transactions_as_gephi = True
		username = marcos
		username_allow_nsfw_scan = True
		username_print_result = True
		username_show_all = False
		username_enable_dump_file = True
	[+] temp_file_manager.TempFileManager
 		Checking Age data/temp/state for 31557600 seconds
 		Checking Age data/temp/bitcoin_wallet for 604800 seconds
 		Checking Age data/temp/username_search for 604800 seconds
	[+] state_file_handler.LoadStateFileHandler
	[+] http_navigation_manager.HttpNavigationManagerHandler
	[+] bitcoin_wallet.BitcoinWalletInfoDownloader
		Target BTC Wallet Empty.
	[+] bitcoin_wallet.BitcoinWalletTransactionsDownloader
	[+] bitcoin_wallet_graph.BitcoinWalletGraphGenerator
		Target BTC Wallet Empty.
	[+] username_handler.UsernameScanner
		NSFW Sites Allowed.
		Starting Scan with 20 Workers.
		7Cups: Claimed > https://www.7cups.com/@marcos
		9GAG: Claimed > https://www.9gag.com/u/marcos
		About.me: Claimed > https://about.me/marcos
		Academia.edu: Claimed > https://independent.academia.edu/marcos
		Asciinema: Claimed > https://asciinema.org/~marcos
		AskFM: Claimed > https://ask.fm/marcos
		Atom Discussions: Claimed > https://discuss.atom.io/u/marcos/summary
		Audiojungle: Claimed > https://audiojungle.net/user/marcos
		Avizo: Claimed > https://www.avizo.cz/marcos/
		BLIP.fm: Claimed > https://blip.fm/marcos
		Bandcamp: Claimed > https://www.bandcamp.com/marcos
		Behance: Claimed > https://www.behance.net/marcos
		BitBucket: Claimed > https://bitbucket.org/marcos/
		Blogger: Claimed > https://marcos.blogspot.com
		BodyBuilding: Claimed > https://bodyspace.bodybuilding.com/marcos
		Bookcrossing: Claimed > https://www.bookcrossing.com/mybookshelf/marcos/
		BuzzFeed: Claimed > https://buzzfeed.com/marcos
		CNET: Claimed > https://www.cnet.com/profiles/marcos/
		CapFriendly: Claimed > https://www.capfriendly.com/users/marcos
		Carbonmade: Claimed > https://marcos.carbonmade.com
		Career.habr: Claimed > https://career.habr.com/marcos
		Championat: Claimed > https://www.championat.com/user/marcos
		Chatujme.cz: Claimed > https://profil.chatujme.cz/marcos
		Cloob: Claimed > https://www.cloob.com/name/marcos
		Codecademy: Claimed > https://www.codecademy.com/profiles/marcos
		Codechef: Claimed > https://www.codechef.com/users/marcos
		Coroflot: Claimed > https://www.coroflot.com/marcos
		DEV Community: Claimed > https://dev.to/marcos
		Designspiration: Claimed > https://www.designspiration.net/marcos/
		DeviantART: Claimed > https://marcos.deviantart.com
	[+] state_file_handler.SaveStateFileHandler


```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/guibacellar/OSIx/issues) for a list of proposed features (and known issues).


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
