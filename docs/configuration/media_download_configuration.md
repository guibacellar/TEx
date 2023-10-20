# Media Download - Configuration

You can customize (fully enabled, disable or selective enable) media download, just specify these settings on  configuration file.

**Enable / Disable Default Media Download Behaviour**
```ini
[MEDIA.DOWNLOAD]
default=ALLOW
max_download_size_bytes=256000000
```

* **default** > Required - Set the default behaviour. Enable (ALLOW) of Disable (DISALLOW)
* **max_download_size_bytes** > Optional - Max download size for all medias in bytes
     * Default: 256000000

**Per Media Setting**
Use *MEDIA.DOWNLOAD.<content-type>* to specify the settings for each individual content-type.
```ini
[MEDIA.DOWNLOAD.<content-type>]
enabled=ALLOW
max_download_size_bytes=256000000
groups=*
```

* **enabled** > Required - Enable/Disable this Content-Type download. Enable (ALLOW) of Disable (DISALLOW)
* **max_download_size_bytes** > Optional - Max download size for this Content-Type
    * Default: 256000000
* **groups** > Optional - If present, Download the Messages only from Specified Groups ID's. Comma Separated. For All Groups, use *
    * Default: * 
