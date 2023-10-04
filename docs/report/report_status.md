# Internal Status Report

Telegram Explorer allow you to generate HTML report containing messages, assets (images, videos, binaries, etc) from groups. Also, you may specify groups, period and message filters to generate a more customized report.

**Full Command:**

```bash
python3 -m TEx stats --config CONFIGURATION_FILE_PATH --report_folder REPORT_FOLDER_PATH --limit_days 3
```

**Parameters**

  * **config** > Required - Created Configuration File Path
  * **report_folder** > Required - Defines the Report Files Folder
  * **limit_days** > Optional - Number of Days of past to filter the Report

*Output Example:*
![report_stats.png](../media/report_stats.png)