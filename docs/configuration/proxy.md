# Proxy
If you need to use a proxy server, you can configure this behavior within the configuration file. If not, just omit this section from your file.

```ini
[PROXY]
type=HTTP
address=127.0.0.1
port=3128
username=proxy username
password=proxy password
rdns=true
```

* **type** > Required - Protocol to use (HTTP, SOCKS5 or SOCKS4)
* **address** > Required - Proxy Address
* **port** > Required - Proxy IP Port
* **username** > Optional - Username if the proxy requires auth
* **password** > Optional - Password if the proxy requires auth
* **rdns** > Optional - Whether to use remote or local resolve, default remote
