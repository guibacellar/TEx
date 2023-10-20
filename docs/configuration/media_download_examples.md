# Media Download - Examples

### Default Behaviour (Download All Medias)
```ini
[MEDIA.DOWNLOAD]
default=ALLOW
max_download_size_bytes=256000000
```

### Download Only Images from All Groups
```ini
[MEDIA.DOWNLOAD]
default=DISALLOW

[MEDIA.DOWNLOAD.image/gif]
enabled=ALLOW
max_download_size_bytes=256000000
groups=*

[MEDIA.DOWNLOAD.image/jpeg]
enabled=ALLOW
max_download_size_bytes=256000000
groups=*

[MEDIA.DOWNLOAD.image/png]
enabled=ALLOW
max_download_size_bytes=256000000
groups=*

[MEDIA.DOWNLOAD.image/webp]
enabled=ALLOW
max_download_size_bytes=256000000
groups=*
```

### Download All Medias, Except Compressed Ones
```ini
[MEDIA.DOWNLOAD]
default=ALLOW
max_download_size_bytes=256000000

[MEDIA.DOWNLOAD.application/rar]
enabled=DISALLOW

[MEDIA.DOWNLOAD.application/vnd.rar]
enabled=DISALLOW

[MEDIA.DOWNLOAD.application/x-7z-compressed]
enabled=DISALLOW

[MEDIA.DOWNLOAD.application/x-compressed-tar]
enabled=DISALLOW

[MEDIA.DOWNLOAD.application/application/zip]
enabled=DISALLOW
```

### Download All Medias, but Compressed Ones only from two groups (id=1234 and id=5678)
```ini
[MEDIA.DOWNLOAD]
default=ALLOW
max_download_size_bytes=256000000

[MEDIA.DOWNLOAD.application/rar]
enabled=DISALLOW
groups=1234,5678

[MEDIA.DOWNLOAD.application/vnd.rar]
enabled=DISALLOW
groups=1234,5678

[MEDIA.DOWNLOAD.application/x-7z-compressed]
enabled=DISALLOW
groups=1234,5678

[MEDIA.DOWNLOAD.application/x-compressed-tar]
enabled=DISALLOW
groups=1234,5678

[MEDIA.DOWNLOAD.application/application/zip]
enabled=DISALLOW
groups=1234,5678
```