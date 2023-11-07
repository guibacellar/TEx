# Notification System - Elastic Search Connector - Signals Template

In order to use the Signal Notification with Elastic Search, you should create a new Index Template before start sending the Signals.

This will help you to get the best of all signals provided.

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
      "content": {
        "type": "text",
        "fielddata": true,
        "fielddata_frequency_filter": {
          "min": 0.01,
          "max": 1,
          "min_segment_size": 50
        }
      },
      "signal": {
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
      }
    }
  },
  "aliases": {}
}
```
