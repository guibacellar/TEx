# Maintenance - Purge Old Data

As any system or application that uses a database to store information, Telegram Explorer needs, eventually, database maintenance to ensure proper work and remove old data.

Our maintenance command purge all old messages and media from database and filesystem.
n messages.

> NOTE: While other commands can be executed side-by-side, or, simultaneously, the 'purge_old_data' command needs to be executed alone, so, stop all TeX instances that uses the same configuration file, specially the 'listen' command before perform the maintenance.

**Full Command:**

```bash
python3 -m TEx purge_old_data --config CONFIGURATION_FILE_PATH --limit_days 30
```
**Parameters**

  * **config** > Required - Created Configuration File Path
  * **limit_days** > Optional - Number of Days of past to remove the messages and files.
