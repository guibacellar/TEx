# Configuration
The basic configuration contains exactly 4 settings:

```ini
[CONFIGURATION]
api_id=my_api_id
api_hash=my_api_hash
phone_number=my_phone_number
data_path=my_data_path
device_model=device_model_name
```

* **api_id** > Required - Telegram API ID. From https://my.telegram.org/ > login > API development tools 
* **api_hash** > Required - Telegram API Hash. From https://my.telegram.org/ > login > API development tools
* **phone_number** > Required - Target Phone Number
* **data_path** > Required - Defines the Path Folder for the SQLite Databases and Dowloaded Files
* **device_model** > Optional - Defines which device model is passed to Telegram Servers.
    * If Blank or Absent - Uses 'TeX' for backwards compatibility
    * If set as 'AUTO' - Uses the computer/system device model

!!! warning "Note about 'device_model'"

    If you are using versions prior to 0.2.15 or have already connected to Telegram and have not configured the 'device_model' parameter, do not make the change, as Telegram may interpret this operation as an attack on your account.

Place the configuration file anywhere you want with .config extension.

**EXAMPLE (myconfig.config)**
```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64
```
