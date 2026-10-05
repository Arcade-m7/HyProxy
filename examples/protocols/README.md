# Protocols Examples

Protocols define how clients communicate with the proxy.

## What are Protocols?

Protocols:
- Handle client connections
- Parse client requests
- Send responses to clients
- Inherit from BaseProtocol

## Supported Protocols

### HTTP/1.1
- Used for: Web browsing
- Port: 80 (standard)
- Format: Text-based
- Features: Most compatible

### SOCKS4
- Used for: Legacy applications
- Port: 1080 (standard)
- Format: Binary protocol
- Features: Minimal overhead

### SOCKS5
- Used for: Modern applications
- Port: 1080 (standard)
- Format: Binary protocol
- Features: Authentication, IPv6

## Files

### 01_http_protocol.py
HTTP/1.1 protocol only.

```bash
python 01_http_protocol.py
```

Features:
- HTTP requests only
- Standard web proxy
- Port 80
- Text-based protocol

Use Case:
- Web browsing
- HTTP applications
- Legacy web clients

### 02_socks4_protocol.py
SOCKS4 protocol only.

```bash
python 02_socks4_protocol.py
```

Features:
- Legacy SOCKS
- Binary protocol
- No authentication
- IPv4 only
- Minimal overhead

Use Case:
- Old applications
- Compatibility needs
- Resource-constrained systems

### 03_socks5_protocol.py
SOCKS5 protocol only.

```bash
python 03_socks5_protocol.py
```

Features:
- Modern SOCKS
- Binary protocol
- Optional authentication
- IPv4 and IPv6
- UDP support

Use Case:
- Modern applications
- Best compatibility
- IPv6 support needed

### 04_mixed_protocols.py
All three protocols on one port.

```bash
python 04_mixed_protocols.py
```

Features:
- Auto-detection
- All protocols simultaneously
- Single port (1968)
- Transparent routing

Use Case:
- Unified proxy
- Unknown client type
- Maximum compatibility

## Protocol Detection

When client connects, first byte determines protocol:

```python
0x04        → SOCKS4
0x05        → SOCKS5
anything    → HTTP
```

## Protocol Classes

### HTTP1O1

```python
from hyproxy.protocols import HTTP1O1

config = Config()
protocol = HTTP1O1(config)

listener = Asynclestener(
    ...,
    protocols=[HTTP1O1(config)]
)
```

### SOCKS4

```python
from hyproxy.protocols import SOCKS4

config = Config()
protocol = SOCKS4(config)

listener = Asynclestener(
    ...,
    protocols=[SOCKS4(config)]
)
```

### SOCKS5

```python
from hyproxy.protocols import SOCKS5

config = Config()
protocol = SOCKS5(config)

listener = Asynclestener(
    ...,
    protocols=[SOCKS5(config)]
)
```

## Configuration Per Protocol

### Different Config Per Protocol

```python
# HTTP with one config
http_config = Config()
http_config.auth.setusername(b'http_user')

# SOCKS with different config
socks_config = Config()
socks_config.auth.setusername(b'socks_user')

listener = Asynclestener(
    ...,
    protocols=[
        HTTP1O1(http_config),
        SOCKS5(socks_config)
    ]
)
```

### Shared Config

```python
config = Config()
config.auth.setusername(b'admin')

listener = Asynclestener(
    ...,
    protocols=[
        HTTP1O1(config),
        SOCKS4(config),
        SOCKS5(config)
    ]
)
```

## Protocol Comparison

| Feature | HTTP/1.1 | SOCKS4 | SOCKS5 |
|---------|----------|--------|--------|
| **Web Browsing** | ✓ | ✗ | ✓ |
| **Authentication** | ✗ | ✗ | ✓ |
| **IPv6** | ✓ | ✗ | ✓ |
| **UDP** | ✗ | ✗ | ✓ |
| **Binary** | ✗ | ✓ | ✓ |
| **Text** | ✓ | ✗ | ✗ |
| **Age** | Modern | Legacy | Modern |

## Learning Path

1. Start with **04_mixed_protocols.py**
2. Try **01_http_protocol.py**
3. Study **03_socks5_protocol.py**
4. Explore **02_socks4_protocol.py**

## Common Setups

### Simple HTTP Proxy

```python
config = Config()
listener = Asynclestener(
    name='HTTPProxy',
    ip='127.0.0.1',
    port=8080,
    protocols=[HTTP1O1(config)]
)
```

### Universal SOCKS

```python
config = Config()
listener = Asynclestener(
    name='SOCKSProxy',
    ip='127.0.0.1',
    port=1080,
    protocols=[SOCKS4(config), SOCKS5(config)]
)
```

### All Protocols

```python
config = Config()
listener = Asynclestener(
    name='UniversalProxy',
    ip='0.0.0.0',
    port=1968,
    protocols=[
        HTTP1O1(config),
        SOCKS4(config),
        SOCKS5(config)
    ]
)
```

## Key Concepts

### Auto-Detection
- Works transparently
- Client unaware of others
- Single port possible
- No client reconfiguration

### Protocol Independence
- Each has own rules
- Different features
- All use Config
- All use BaseProtocol

### Mixed Deployments
- Support legacy systems
- Support modern clients
- Single infrastructure
- Simplified management

## Notes

- Each protocol inherits from BaseProtocol
- Config applies to all protocols
- Auto-detection first byte
- All protocols run simultaneously

## Reference

For implementation details:
- HTTP: `hyproxy/protocols/http/main.py`
- SOCKS4: `hyproxy/protocols/socks4.py`
- SOCKS5: `hyproxy/protocols/socks5.py`
- Base: `hyproxy/protocols/base.py`
