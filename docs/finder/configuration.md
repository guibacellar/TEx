# Message Finder System

**Compatibility:** Message Listener Command

Telegram Explorer allows to specify many message finders. Usually, the finder engine looks at messages, but, they also can look at downloaded text files (plain, csv, xml, json, etc.). 

**Configuration Spec:**

In order to use the finder engine, you must set a configuration to enable-it and configure if you want to allow the engine to find on files.

**Parameters:**

  * **enabled** > Required - Enable(true)/Disable(false) the finder engine.
  * **find_in_text_files_enabled** > Optional - Enable(true)/Disable(false) the behavior that run the finder engine inside the downloaded files.
    * Default: false
  * **find_in_text_files_max_size_bytes** > Optional - Set the max size in bytes of file that allow the engine to load the file in memory and perform the searches.
    * Default: 10000000


**Changes on Configuration File**
```ini
[FINDER]
enabled=true
find_in_text_files_enabled=true
find_in_text_files_max_size_bytes=20000000
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