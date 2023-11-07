# Notification System - Signals

Signals are the way that Telegram Explorer report some internal behaviors and events.

Currently, there are 4 unique signals:

  - **Initialization** - Happens everytime the Telegram Explorer starts the 'listen' command
  - **Keep Alive** - Sent every (keep_alive_interval) seconds while the Telegram Explorer are running the 'listen' command
  - **New Group** - Happen everytime when the 'listen' command receive a new group for first time
  - **Shutdown** - Happens everytime the Telegram Explorer finish the 'listen' command

**Configuration Spec:**

You are able to fully enable/disable the signal system and have a fine control on each signal. 

Also, Signals works like any notification from Telegram Explorer and you can configure each signal individually to be sent on any supported Notification Engines.

!!! info "Use Separated Notifiers"
    
    Although you can use the same notifiers that you use for finder mechanisms, we strong recommend to create a dedicated configuration to use the signals, specially if you are going to use on Elastic Search, because Telegram Explorer have a new and dedicated Index Template for this.

**Elastic Search Signals Index Template:** [Check the Template Here](notification_elasticsearch_signals_template.md)

**Parameters:**

  * **enabled** > Required - Enable/Disable the Signals System
  * **keep_alive_interval** > Required - Time (in seconds) that the system goes to sent the KEEP-ALIVE signal
  * **keep_alive_notifer** > Optional - Name of notifiers to be used to receive the KEEP-ALIVE signal (comma separated). Supress to Disable this Signal
  * **initialization_notifer** > Optional - Name of notifiers to be used to receive the INITIALIZATION signal (comma separated). Supress to Disable this Signal
  * **shutdown_notifer** > Optional - Name of notifiers to be used to receive the SHUTDOWN signal (comma separated). Supress to Disable this Signal
  * **new_group_notifer** > Optional - Name of notifiers to be used to receive the NEW-GROUP signal (comma separated). Supress to Disable this Signal


**Changes on Configuration File**
```ini
[SIGNALS]
enabled=true
keep_alive_interval=300

keep_alive_notifer=NOTIFIER.ELASTIC_SEARCH.ELASTIC_INDEX_01
initialization_notifer=NOTIFIER.ELASTIC_SEARCH.ELASTIC_INDEX_01,NOTIFIER.DISCORD.MY_HOOK_2
shutdown_notifer=NOTIFIER.ELASTIC_SEARCH.ELASTIC_INDEX_01,NOTIFIER.DISCORD.MY_HOOK_2
new_group_notifer=NOTIFIER.DISCORD.MY_HOOK_2 
```
