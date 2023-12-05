# Message Finder System

**Compatibility:** Message Listener Command

Telegram Explorer allows to specify many message finders. Usually, the finder engine looks at messages, but, they also can look at downloaded text files (plain, csv, xml, json, etc.).

It's through the Finder engine that you are able to send notifications or export the chat contents (Check the *Notification System* and *Message Export System* for more information).

**Configuration Spec:**

In order to use the finder engine, you must set a configuration to enable-it and configure if you want to allow the engine to find on files.

**Parameters:**

  * **enabled** > Required - Enable(true)/Disable(false) the finder engine.
  * **find_in_text_files_enabled** > Optional - Enable(true)/Disable(false) the behavior that run the finder engine inside the downloaded files.
    * Default: false
  * **find_in_text_files_max_size_bytes** > Optional - Set the max size in bytes of file that allow the engine to load the file in memory and perform the searches.
    * Default: 10000000
  * **notifier** > Optional - The list of all (comma separated) notifiers that runs when the finder triggers.
  * **exporter** > Optional - The list of all (comma separated) file exporters that runs when the finder triggers.


**Changes on Configuration File**
```ini
[FINDER]
enabled=true
find_in_text_files_enabled=true
find_in_text_files_max_size_bytes=20000000
notifier=NOTIFIER.DISCORD.MY_HOOK_1,NOTIFIER.DISCORD.MY_HOOK_2
exporter=EXPORTER.ROLLING_PANDAS.MY_EXPORTER_1,EXPORTER.ROLLING_PANDAS.MY_EXPORTER_2
```

**Files Supported for the Engine:**

  * application/atom+xml
  * application/bittorrent
  * application/csv
  * application/html
  * application/json
  * application/ld+json
  * text/csv
  * text/html
  * text/plain
  * text/xml