# Message Finder System - RegEx

**Compatibility:** Message Listener Command

Telegram Explorer allows to specify many message finders using Regular Expressions. 

Each time one Finder rule match, the system automatically uses the Notification System to report that message.

Every Finder is defined in the configuration files.

**Configuration Spec:**

For each rule to be used, you must set a configuration using the default name schema *FINDER.RULE.<RULE_NAME>*

**Parameters:**

  * **type** > Required - Fixed Value 'regex'
  * **regex** > Required - The regular expression. You can also use one regex per Line
  * **notifier** > Required - Name of notifiers to be used to notify the triggered message (comma separated).

**Changes on Configuration File**
```ini
[FINDER]
enabled=true

[FINDER.RULE.MessagesWithURL]
type=regex
regex=/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%%_\+.~#?&\/=]*)$/
notifier=NOTIFIER.DISCORD.MY_HOOK_1

[FINDER.RULE.FindMessagesWithCreditCard]
type=regex
regex=(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
notifier=NOTIFIER.DISCORD.MY_HOOK_1,NOTIFIER.DISCORD.MY_HOOK_2

[FINDER.RULE.MultipleRegEx]
type=regex
regex=
    /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%%_\+.~#?&\/=]*)$/
    (^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
notifier=NOTIFIER.DISCORD.MY_HOOK_1,NOTIFIER.DISCORD.MY_HOOK_2
```