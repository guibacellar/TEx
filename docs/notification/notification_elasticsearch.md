# Notification System - Elastic Search Connector

Telegram Explorer allows to send notifications to Elastic Search through ingestion API.

Every Notification is defined in the configuration files.

!!! info "Elastic Search Compatibility"
    
    Tested on Elastic Search 8+

!!! warning "Index Template"
    
    If you want, and we recommend, create a new Index Template before create your indexes. Please, check on "Notification System" > "Elastic Search Connector" > "Index Template" and "Signals Template" for more information.

**Configuration Spec:**

For each connector you must set a configuration using the default name schema *NOTIFIER.ELASTIC_SEARCH.<NAME>*

**Parameters:**

  * **address** > Optional - Elastic Search Address. Multiple values comma separated.
  * **api_key** > Required - Elastic Search API Key.
  * **cloud_id** > Optional - Elastic Search Cloud ID.
  * **verify_ssl_cert** > Optional - Configure if the connector checks the SSL cert. Default=True
  * **index_name** > Required - Elastic Search Index Name.
  * **pipeline_name** > Required - Elastic Search Ingestion Pipeline Name.


**Changes on Configuration File (with Address)**
```ini
[NOTIFIER.ELASTIC_SEARCH.ELASTIC_INDEX_01]
address=https://elastic_search_url_1:9200,https://elastic_search_url_2:9200
api_key=bHJtVEg0c0JnNkwwTnYtYTFdeadbeefrXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=False
index_name=search-telegram_explorer
pipeline_name=ent-search-generic-ingestion
```

**Changes on Configuration File (with Cloud ID)**
```ini
[NOTIFIER.ELASTIC_SEARCH.ELASTIC_INDEX_02]
cloud_id=deployment-name:dXMtZWFzdDQuZ2Nw
api_key=bHJtVEg0c0JnNkwwTnYtYTFdeadbeefrXzd6NVFSUmEtQ21mQldiUjEwUQ==
verify_ssl_cert=True
index_name=search-telegram_explorer
pipeline_name=ent-search-generic-ingestion
```
