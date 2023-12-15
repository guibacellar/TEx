# Notification System - Elastic Search Connector - Signals Template

In order to use the Signal Notification with Elastic Search, you should create a new Index Template before start sending the Signals.

This will help you to get the best of all signals provided.

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
    "source": {
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
    },
    "signal": {
      "eager_global_ordinals": false,
      "index_phrases": false,
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "norms": true,
      "index": true,
      "store": false,
      "type": "text",
      "index_options": "positions"
    },
    "content": {
      "eager_global_ordinals": false,
      "index_phrases": false,
      "fielddata_frequency_filter": {
        "min": 0.01,
        "max": 1,
        "min_segment_size": 50
      },
      "fielddata": true,
      "norms": true,
      "index": true,
      "store": false,
      "type": "text",
      "index_options": "positions"
    }
  }
}
```
