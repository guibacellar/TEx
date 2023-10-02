
### Generate Report
Generate HTML Report
```bash
python3 -m TEx report --config CONFIGURATION_FILE_PATH --report_folder REPORT_FOLDER_PATH --group_id * --around_messages NUM --order_desc --limit_days 3 --filter FILTER_EXPRESSION_1,FILTER_EXPRESSION_2,FILTER_EXPRESSION_N
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **around_messages** > Optional - Number of messages around (Before and After) the Filtered Message
  * **order_desc** > Optional - If present, sort all messages descending. Otherwise, sort Ascending.
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **filter** > Optional - Simple (Comma Separated) String Terms Filter. Ex: hacking,"Car Hacking",foo
  * **suppress_repeating_messages** > Optional - If present, suppress all repeating messages in the same report

### Export Downloaded Files
Export Downloaded Files by MimeType
```bash
python3 -m TEx export_file --config CONFIGURATION_FILE_PATH -report_folder REPORT_FOLDER_PATH --group_id * --filter * --limit_days 3 --mime_type text/plain
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **filter** > Optional - Simple (Comma Separated) FileName String Terms Filter. Ex: malware, "Bot net"
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **mime_type** > Optional - File MIME Type. Ex: application/vnd.android.package-archive

### Export Texts
Export Messages (Texts) using Regex finder
```bash
python3 -m TEx export_text --config CONFIGURATION_FILE_PATH --order_desc --limit_days 3 --regex REGEX --report_folder REPORT_FOLDER_PATH --group_id *
```
  * **config** > Required - Created Configuration File Path
  * **report_folder** > Optional - Defines the Report Files Folder
  * **group_id** > Optional - If present, Download the Messages only from Specified Groups ID's
  * **limit_days** > Optional - Number of Days of past to filter the Messages
  * **regex** > Required - Regex to find the messages. 
    * Ex: Export Links from Messages (.*http://.*),(.*https://.*)
