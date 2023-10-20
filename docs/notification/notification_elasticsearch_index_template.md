# Notification System - Elastic Search Connector - Index Template

If you want, create a new Index Template before create all Telegram Explorer indexes.

This will help you to get the best of all data provided and allow's to extract many more value and informations from the data.

**Index Template JSON**
```json
{
  "settings": {
    "index": {
      "routing": {
        "allocation": {
          "include": {
            "_tier_preference": "data_content"
          }
        }
      }
    }
  },
  "mappings": {
    "dynamic": "true",
    "dynamic_date_formats": [
      "strict_date_optional_time",
      "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
    ],
    "dynamic_templates": [],
    "date_detection": true,
    "numeric_detection": false,
    "properties": {
      "from_id": {
        "type": "long"
      },
      "group_id": {
        "type": "long"
      },
      "group_name": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "has_media": {
        "type": "boolean"
      },
      "is_reply": {
        "type": "boolean"
      },
      "media_mime_type": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "media_size": {
        "type": "long"
      },
      "message_id": {
        "type": "text"
      },
      "raw": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "reply_to_msg_id": {
        "type": "long"
      },
      "rule": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "source": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "time": {
        "type": "date"
      },
      "to_id": {
        "type": "long"
      }
    }
  },
  "aliases": {}
}
```
