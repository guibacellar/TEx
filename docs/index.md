# Welcome to Telegram Explorer

[![](https://img.shields.io/github/last-commit/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/github/languages/code-size/guibacellar/TEx)](https://github.com/guibacellar/TEx/tree/main)
[![](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/downloads/) 
[![](https://github.com/guibacellar/TEx/actions/workflows/cy.yml/badge.svg?branch=main)](https://github.com/guibacellar/TEx/actions/workflows/cy.yml)
[![](https://telegramexplorer.readthedocs.io/en/latest/?badge=latest)](https://telegramexplorer.readthedocs.io/en/latest/)
[![](https://img.shields.io/badge/maintainer-Th3%200bservator-blue)](https://theobservator.net/)
![](https://img.shields.io/github/v/release/guibacellar/TeX)

<!-- ABOUT THE PROJECT -->
## About The Project

TEx is a Telegram Explorer tool created to help Researchers, Investigators and Law Enforcement Agents to Collect and Process the Huge Amount of Data Generated from Criminal, Fraud, Security and Others Telegram Groups.

Repository: [https://github.com/guibacellar/TEx](https://github.com/guibacellar/TEx)

!!! warning "BETA VERSION"
    
    Please note that this project has been in beta for a few weeks, so it is possible that you may encounter bugs that have not yet been mapped out.
    I kindly ask you to report the bugs at: [https://github.com/guibacellar/TEx/issues](https://github.com/guibacellar/TEx/issues)

<!-- REQUIREMENTS -->
## Requirements
- Python 3.8.1+ (⚠️ Deprecated. Consider using version 3.10+ ⚠️)
- Windows x64 or Linux x64

<!-- FEATURES -->
## Features
- Connection Manager (Handle Telegram Connection)
- Group Information Scrapper
- List Groups (Scrap info for all groups, including members, members info and profile pic)
- Automatic Group Information Sync
- Automatic Users Information Sync
- Messages Listener (Listen all Incoming Messages)
- Messages Scrapper (Scrap all Group Messages, since the first one)
- Download Media (Including fine media settings like size, groups and/or media type)
- HTML Report Generation
- Export Downloaded Files
- Export Messages
- Message Finder System (Allow to Find, using terms or RegEx) patterns on messages
- Message Notification System (Send alert's, finds, or all messages to Discord)
- Elastic Search 8+ Native Integration
- Image OCR using Tesseract

<!-- LIMITATIONS -->
## Know Limitations

Although we do not currently know the limitations of using the tool, it is important to announce the limits to which we test the platform.

Currently, **one TeX process can support at least** (per configuration file/per phone numer):

**Per Group**

- 50,000 messages
- 7,000 users per group
- 8 GB of downloaded files

**Total**

- 400 groups
- 800,000 messages
- 50,000 unique users
- 150 GB of total downloaded files

<!-- HOW WORKS -->
## How Telegram Explorer Works
Telegram Explorer works using one configuration file per target phone number to be used. 

![how_text_works.png](media/how_text_works.png)

So, you can deploy 1 or several Telegram Explorer runners in one machine, using on configuration file for each instance. You also can deploy the runner using Linux Containers or Docker containers.

!!! info "IMPORTANT"
    
    Depending on the security level and your account settings, you may be asked to enter a security code that will be sent to your Telegram, or some authentication information. </br></br>This way, the application will ask (only at the time of the first connection) for you to enter this value in the terminal (TTY).

<!-- INSTALLING -->
## Installing
Telegram Explorer is available through *pip*, so, just use pip install in order to fully install TeX.

```bash
pip install TelegramExplorer
```

<!-- Upgrading -->
## Upgrading
To upgrade TeX to the latest version, just use *pip install upgrade* command.

```bash
pip install --upgrade TelegramExplorer
```
