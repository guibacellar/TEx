# Generate Report - HTML

Telegram Explorer exports a internal status report containing statistics about message and users count for each group, also a media info with size and content-type.

**Full Command:**

```bash
python3 -m TEx export_text --config CONFIGURATION_FILE_PATH --order_desc --limit_days 3 --regex REGEX --report_folder REPORT_FOLDER_PATH --group_id 12547,1256698
```

**Basic Command:**

```bash
python3 -m TEx export_text --config CONFIGURATION_FILE_PATH --limit_days 3 --regex REGEX --report_folder REPORT_FOLDER_PATH
```
**Parameters**

  * **config** > Required - Created Configuration File Path
  * **report_folder** > Required - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **regex** > Required - Regex to find the messages. 
    * Ex: Export Links from Messages (.\*http://.\*),(.\*https://.\*)

*Output Example Using "*(.\*http://.\*),(.\*https://.\*)*" Regular Expression:*

*Report Folder*
![text_report_files.png](../media/text_report_files.png)

*File Content*
![text_report_content.png](../media/text_report_content.png)