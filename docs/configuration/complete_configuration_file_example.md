# Complete Configuration File Example

This is an example of a complete configuration file with four finder rules using three discord hooks, two elastic search connector and signals configuration.

```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64
timeout=30

[PROXY]
type=HTTP
address=127.0.0.1
port=3128
username=proxy username
password=proxy password
rdns=true

[MEDIA.DOWNLOAD]
default=ALLOW
max_download_size_bytes=256000000

[FINDER]
enabled=true

[FINDER.RULE.MessagesWithURL]
type=regex
regex=/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/
notifier=NOTIFIER.DISCORD.MY_HOOK_1

[FINDER.RULE.FindMessagesWithCreditCard]
type=regex
regex=(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
notifier=NOTIFIER.DISCORD.MY_HOOK_2,NOTIFIER.ELASTIC_SEARCH.GENERAL

[FINDER.RULE.FindMessagesWithEmail]
type=regex
regex=^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$
notifier=NOTIFIER.DISCORD.MY_HOOK_1,NOTIFIER.DISCORD.MY_HOOK_2

[FINDER.RULE.CatchAll]
type=all
notifier=NOTIFIER.ELASTIC_SEARCH.GENERAL
exporter=EXPORTER.ROLLING_PANDAS.EXPORT_ALL_MESSAGES

[FINDER.RULE.DefangsUrls]
type=regex
regex=/^hXXp:\/\/(?:[A-Za-z0-9_.-]+\[.\])+[A-Za-z]+\/?$/
notifier=NOTIFIER.ELASTIC_SEARCH.GENERAL

[NOTIFIER.DISCORD.MY_HOOK_1]
webhook=https://discord.com/api/webhooks/1157896186751897357/o7foobar4txvAvKSdeadHiI-9XYeXaGlQtd-5PtrrX_eCE0XElWktpPqjrZ0KbeefPtQC
prevent_duplication_for_minutes=240
timeout_seconds=30
media_attachments_enabled=false

[NOTIFIER.DISCORD.MY_HOOK_2]
webhook=https://discord.com/api/webhooks/1128765187657681875/foobarqOMFp_4tM2ic2mbeefNPOZqJnBZZdfaubQv2vJgbYzfdeadZd5aqGX6FmCmbNjX
prevent_duplication_for_minutes=240
media_attachments_enabled=false

[NOTIFIER.DISCORD.SIGNALS_HOOK]
webhook=https://discord.com/api/webhooks/1128765187657681875/foobarqOMFp_457EDs2mbeefNPPeqJnBZZdfaubQvOKIUHYzfdeadZd5aqGX6FmCmbNjv
prevent_duplication_for_minutes=0
media_attachments_enabled=true
media_attachments_max_size_bytes=10000000

[NOTIFIER.ELASTIC_SEARCH.GENERAL]
address=https://localhost:9200
api_key=bHJtVEg0c0JnNkwwTnYtFFDEADlo6NS1rXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=False
index_name=index-name
pipeline_name=ent-search-generic-ingestion

[NOTIFIER.ELASTIC_SEARCH.SIGNALS]
address=https://localhost:9200
api_key=bHJtVEg0c0JnNkwwTnYtFFDEADlo6NS1rXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=False
index_name=index-name-for-signals
pipeline_name=ent-search-generic-ingestion

[EXPORTER.ROLLING_PANDAS.EXPORT_ALL_MESSAGES]
file_root_path=/path/to/export/folder/
rolling_every_minutes=5
fields=date_time,raw_text,group_name,group_id,from_id,to_id,reply_to_msg_id,message_id,is_reply,found_on
use_header=true
output_format=json
keep_last_files=20

[OCR]
enabled=true
type=tesseract

[OCR.TESSERACT]
tesseract_cmd=/path/to/tesseract/cmd
language=eng

[SIGNALS]
enabled=true
keep_alive_interval=300

keep_alive_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
initialization_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
shutdown_notifer=NOTIFIER.ELASTIC_SEARCH.SIGNALS
new_group_notifer=NOTIFIER.DISCORD.SIGNALS_HOOK,NOTIFIER.ELASTIC_SEARCH.SIGNALS
```
