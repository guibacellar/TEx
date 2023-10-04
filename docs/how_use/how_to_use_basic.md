# Basic Usage

## The Basics
Considering a *my_TEx_config.config* file created at */usr/my_TEx_config.config* with follow:

```editorconfig
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
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

### Listen Messages (Start the Message Listener)
```bash
python3 -m TEx listen --config CONFIGURATION_FILE_PATH --group_id 1234,5678
```

  * **config** > Required - Created Configuration File Path
  * **ignore_media** > Optional - If present, don't Download any Media
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
