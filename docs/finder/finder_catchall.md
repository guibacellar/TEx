# Message Finder System - Catch All Messages

**Compatibility:** Message Listener Command

Telegram Explorer allows to catch all messages and redirect to one or more notifications connectior. 

**Configuration Spec:**

For each rule to be used, you must set a configuration using the default name schema *FINDER.RULE.<RULE_NAME>*

**Parameters:**

  * **type** > Required - Fixed Value 'all'
  * **notifier** > Required - Name of notifiers to be used to notify the triggered message (comma separated).

**Changes on Configuration File**
```ini
[FINDER]
enabled=true

[FINDER.RULE.CatchAll]
type=all
notifier=NOTIFIER.ELASTIC_SEARCH.GENERAL
```