# Complete Configuration File Example

This is an example of a complete configuration file with three finder rules using two discord hooks.

```ini
[CONFIGURATION]
api_id=12555896
api_hash=dead1f29db5d1fa56cc42757acbabeef
phone_number=15552809753
data_path=/usr/home/tex_data/
device_model=AMD64

[FINDER]
enabled=true

[FINDER.RULE.MessagesWithURL]
type=regex
regex=/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/
notifier=NOTIFIER.DISCORD.MY_HOOK_1

[FINDER.RULE.FindMessagesWithCreditCard]
type=regex
regex=(^4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11}$)
notifier=NOTIFIER.DISCORD.MY_HOOK_2

[FINDER.RULE.FindMessagesWithEmail]
type=regex
regex=^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$
notifier=NOTIFIER.DISCORD.MY_HOOK_1,NOTIFIER.DISCORD.MY_HOOK_2

[NOTIFIER.DISCORD.MY_HOOK_1]
webhook=https://discord.com/api/webhooks/1157896186751897357/o7foobar4txvAvKSdeadHiI-9XYeXaGlQtd-5PtrrX_eCE0XElWktpPqjrZ0KbeefPtQC
prevent_duplication_for_minutes=240

[NOTIFIER.DISCORD.MY_HOOK_2]
webhook=https://discord.com/api/webhooks/1128765187657681875/foobarqOMFp_4tM2ic2mbeefNPOZqJnBZZdfaubQv2vJgbYzfdeadZd5aqGX6FmCmbNjX
prevent_duplication_for_minutes=240
```
