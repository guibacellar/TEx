# Scenario-Based Configuration File Examples

### Sent All Messages to Elasticsearch
```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64
timeout=30

[FINDER]
enabled=true

[FINDER.RULE.CatchAll]
type=all
notifier=NOTIFIER.ELASTIC_SEARCH.GENERAL

[NOTIFIER.ELASTIC_SEARCH.GENERAL]
address=https://localhost:9200
api_key=bHJtVEg0c0JnNkwwTnYtFFDEADlo6NS1rXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=False
index_name=index-name
pipeline_name=ent-search-generic-ingestion
```


### Export All Messages as CSV File
```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64
timeout=30

[FINDER]
enabled=true

[FINDER.RULE.CatchAll]
type=all
exporter=EXPORTER.ROLLING_PANDAS.EXPORT_ALL_MESSAGES

[EXPORTER.ROLLING_PANDAS.EXPORT_ALL_MESSAGES]
file_root_path=/path/to/export/folder/
rolling_every_minutes=5
fields=date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on
use_header=true
output_format=json
keep_last_files=20
```

### Sent Signals to Elasticsearch and Discord
```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64
timeout=30

[FINDER]
enabled=true

[NOTIFIER.DISCORD.SIGNALS_HOOK]
webhook=https://discord.com/api/webhooks/1128765187657681875/foobarqOMFp_457EDs2mbeefNPPeqJnBZZdfaubQvOKIUHYzfdeadZd5aqGX6FmCmbNjv
prevent_duplication_for_minutes=0
media_attachments_enabled=true
media_attachments_max_size_bytes=10000000

[NOTIFIER.ELASTIC_SEARCH.SIGNALS]
address=https://localhost:9200
api_key=bHJtVEg0c0JnNkwwTnYtFFDEADlo6NS1rXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=False
index_name=index-name-for-signals
pipeline_name=ent-search-generic-ingestion

[SIGNALS]
enabled=true
keep_alive_interval=300

keep_alive_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
initialization_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
shutdown_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
new_group_notifer=NOTIFIER.DISCORD.SIGNALS_HOOK,NOTIFIER.ELASTIC_SEARCH.SIGNALS
```
