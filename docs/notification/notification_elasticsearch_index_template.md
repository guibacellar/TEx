# Notification System - Elastic Search Connector - Index Template

If you want, create a new Index Template before create all Telegram Explorer indexes.

This will help you to get the best of all data provided and allow's to extract many more value and informations from the data.

**Index Mapping JSON**
```json
{
  "numeric_detection": false,
  "dynamic_date_formats": [
    "strict_date_optional_time",
    "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
  ],
  "dynamic": "true",
  "dynamic_templates": [],
  "date_detection": true,
  "properties": {
    "from_id": {
      "type": "long"
    },
    "media_size": {
      "type": "long"
    },
    "group_name": {
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "type": "text"
    },
    "reply_to_msg_id": {
      "type": "long"
    },
    "has_media": {
      "type": "boolean"
    },
    "raw": {
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "type": "text"
    },
    "rule": {
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "type": "text"
    },
    "to_id": {
      "type": "long"
    },
    "message_id": {
      "type": "text"
    },
    "source": {
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "type": "text"
    },
    "is_reply": {
      "type": "boolean"
    },
    "found_on": {
      "type": "text"
    },
    "group_id": {
      "type": "long"
    },
    "media_mime_type": {
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "type": "text"
    },
    "time": {
      "type": "date"
    }
  }
}
```
