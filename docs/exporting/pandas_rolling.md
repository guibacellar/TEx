# Message Exporting System - Pandas Rolling Exporter

Telegram Explorer allows to export messages as CSV, XML, JSON or Pickle Serialized Pandas DataFrame almost at real time.

This way you can configure many exporters you want, one for each need or category you like.

!!! warning "NOTE ABOUT THE EXPORTING PROCESS"
    
    This specific exporter only writes the output file when the rolling period terminates, and/or, when Telegram Explorer process stops.

Every Exporter is defined in the configuration files.

**Configuration Spec:**

For each Pandas Rolling Exporter you must set a configuration using the default name schema *EXPORTER.ROLLING_PANDAS.<EXPORTER_NAME\>*

**Parameters:**

  * **file_root_path** > Required - Root path for the exported files.
  * **rolling_every_minutes** > Optional - Time (in minutes) that the system will roll a new file.
    * Default: 30
  * **fields** > Optional - The list (comma separated) with the fields you want to be exported.
    * Default: date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on
  * **use_header** > Optional - Enable/Disable the file header on exported file. 
    * Default: true
  * **output_format** > Optional - Specify the output file format (json, csv, xml and pickle).
    * Default: csv
  * **keep_last_files** > Optional - Specify how many files the engine keep on folder before starts to delete the old ones.
    * Default: 20

**Changes on Configuration File**
```ini
[EXPORTER.ROLLING_PANDAS.MY_EXPORTER_1]
file_root_path=/path/to/export/folder/
rolling_every_minutes=5
fields=date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on
use_header=true
output_format=json
keep_last_files=20

[EXPORTER.ROLLING_PANDAS.MY_EXPORTER_2]
file_root_path=/path/to/export/folder/
rolling_every_minutes=10
fields=date_time,group_id,group_name,raw_text,from_id,to_id,message_id
```
