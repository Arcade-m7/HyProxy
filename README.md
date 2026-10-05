![HyProxy Banner](hyproxy-banner.png)
<h3 align="center">MODERN PROXY SERVER FOR PYTHON</h3>
<p align="center">
  <a href="#HyProxy">HyProxy</a> •
  <a href="#Support">Support</a> •
  <a href="#Features">Features</a> •
  <a href="#Requirements">Requirements</a> •
  <a href="#Installation">Installation</a> •
  <a href="#Examples">Examples</a> •
  <a href="#Documentation
">Documentation</a>
</p>

<br>

# HyProxy

HyProxy is an asynchronous Python proxy module that supports HTTP/1.1, SOCKS4, and SOCKS5 protocols. It is built around `asyncio` and provides configurable policy rules, connection handling, and DNS utilities for proxy tunnel management.

## Support

[<img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" width="150" alt="Buy Me A Coffee" />](https://buymeacoffee.com/Arcade.m7)

## Features

- HTTP/1.1 proxy support
- SOCKS4 and SOCKS5 proxy support
- Policy-driven routing and access control
- Authentication helpers and configurable command filtering
- Async stream/tunnel handling with timeout and byte counters
- DNS cache and resolver utilities

## Requirements

- Python 3.11 or newer
- `aiodns` for async DNS resolution

## Installation

```powershell
pip install HyProxy
```


## Examples

Example 1: create a simple proxy server with HTTP1.1 and SOCKS4 support.

```python
from hyproxy import Server, Asynclestener
from hyproxy.protocols import HTTP1O1, SOCKS4

server = Server(
    Asynclestener(
        name='HyProxy',  # The name of the listener
        ip='127.0.0.1',  # The IP address of the server
        port=1001,  # The port number
        protocols=[  # Supported protocols
            HTTP1O1(),  # HTTP/1.1 support
            SOCKS4(),  # SOCKS4 support
        ]
    )
)

server.run()  # Start the proxy server
```

Then test it with `requests`:

```python
import requests

requests.get(
    'https://www.example.com/',
    proxies={'https': 'http://127.0.0.1:1001'}
)

requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks4://127.0.0.1:1001'}
)

requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks5://127.0.0.1:1001'}
)
```

Example 2: add username/password authentication to proxy protocols.

```python
from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5

# You can use the Config class to customize the proxy, such as setting a username and password.
# Note: the username and password must always be provided as bytes.
config = Config()
config.auth.setusername(b'admin')  # Set the username
config.auth.setpassword(b'admin')  # Set the password

server = Server(
    Asynclestener(
        'HyProxy',
        protocols=[
            HTTP1O1(config),  # Use the configured HTTP handler
            SOCKS4(config),  # Use the configured SOCKS4 handler
            SOCKS5(config),  # Use the configured SOCKS5 handler
        ]
    )
)

server.run()
```

Then test it with `requests`:

```python
import requests

requests.get(
    'https://www.example.com/',
    proxies={'https': 'http://admin:admin@127.0.0.1:1001'}
)

requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks4://admin:admin@127.0.0.1:1001'}
)

requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks5://admin:admin@127.0.0.1:1001'}
)
```

Example 3: block or allow connections by destination port.

```python

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS

config = Config()
config.policy.addrule(
    SimpleRule(
        RouteInfo(dst=NETADDRESS(port=443)),  # Allow only port 443
        '1 RULE',
        ACTIONS.ALLOW
    )
)

# Block any connection to ports in the range 1-5000.
# Port 443 is allowed first, so it is exempt from the deny rule.
config.policy.addrule(
    SimpleRule(
        RouteInfo(dst=NETADDRESS(port=range(1, 5001))),
        '2 RULE',
        ACTIONS.DENY
    )
)

proc = [
    HTTP1O1(config),  # HTTP proxy support
    SOCKS4(config),  # SOCKS4 proxy support
    SOCKS5(config),  # SOCKS5 proxy support
]

server = Server(
    Asynclestener(
        'Config',
        protocols=proc
    )
)

server.run()
```

Then test it with `requests`:

```python
import requests

# When you try to connect to port 80, the proxy server will refuse the connection.
requests.get(
    'http://www.example.com/',
    proxies={'http': 'http://127.0.0.1:1001'}
)

# If you connect to port 443, it will be allowed normally.
requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks4://127.0.0.1:1001'}
)

# Note: any port in the range 1-5000 will be denied, except 443.
requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks5://127.0.0.1:1001'}
)
```

Example 4: use separate configs per protocol.

```python
from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS

config1 = Config()

# Block the website www.example.com by domain name.
config1.policy.addrule(
    SimpleRule(
        RouteInfo(dst=NETADDRESS(domain='www.example.com')),
        'RULE 1',
        ACTIONS.DENY
    )
)

config1.auth.setusername(b"Arcade")  # Username for the first config
config1.auth.setpassword(b"Arcade")  # Password for the first config

config2 = Config()
config2.auth.setusername(b"haytam")  # Username for the second config
config2.auth.setpassword(b"haytam")  # Password for the second config

proc = [
    HTTP1O1(config1),  # HTTP connections will be blocked for www.example.com
    SOCKS4(config2),  # SOCKS4 connections will still be allowed
]

server = Server(
    Asynclestener(
        'Config',
        protocols=proc
    )
)

server.run()
```

Then test it with `requests`:

```python
import requests

requests.get(
    'https://www.example.com/',
    proxies={'https': 'http://Arcade:Arcade@127.0.0.1:1001'}
)  # This will be denied

requests.get(
    'https://www.example.com/',
    proxies={'https': 'socks4://haytam:haytam@127.0.0.1:1001'}
)  # This should work normally
```

> **Note:** HyProxy has not been fully tested yet and may contain bugs or unexpected behavior. Use it carefully, especially in production environments.

> **More examples:** See the [`examples/`](examples/) folder for detailed usage examples and configuration guides.

## Documentation

HyProxy is structured around a small set of cooperating modules.

- `hyproxy/server/`
  - `Asynclestener`: listens on a host/port and accepts incoming TCP clients.
    It wraps each client socket into a `Stream`, inspects the first received bytes, and selects the correct protocol handler.
  - `Server`: manages one or more `Asynclestener` instances and starts the asyncio runtime to serve them concurrently.

- `hyproxy/protocols/`
  - `SOCKS4` and `SOCKS5`: implement the SOCKS handshake, authentication check, and destination request parsing for SOCKS proxies.
    These protocol handlers receive the client connection, build a tunnel, and hand off traffic forwarding to the proxy engine.
  - `HTTP1O1`: implements HTTP/1.1 proxy behavior, parsing HTTP request lines and headers, then forwarding data through the tunnel.

- `hyproxy/conf/`
  - `Config`: the main configuration container used by protocol handlers and the server.
    It holds `auth`, `cmd`, `connection`, `policy`, logging, and optional private/MITM callbacks.
    Use `Config` to enable or disable command support, configure authentication credentials, and set connection timeouts or limits.

- `hyproxy/policy/`
  - `Policy`, `SimpleRule`, `RouteInfo`, `IPADDR`, `IPNET`, and `RULES` define the access-control engine.
    Policies are evaluated for each request route and can allow or deny traffic based on destination IP, port, or domain patterns.

The runtime flow is:
1. `Server` starts one or more `Asynclestener` listeners.
2. `Asynclestener` accepts a connection and selects a protocol via the initial byte inspection.
3. The chosen protocol (`SOCKS4`, `SOCKS5`, or `HTTP1O1`) processes the client request using the shared `Config`.
4. The proxy engine builds a `Tunnel` and forwards traffic between client and destination.
5. `Policy` checks route rules to decide whether the connection is allowed.

