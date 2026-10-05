# Config Socket Examples

Configuration for socket-level network operations and connection management.

## What is Socket Configuration?

Socket configuration controls:
- IP version support (IPv4, IPv6)
- Connection timeouts
- Maximum concurrent connections
- DNS resolution settings

## API Overview

### IPv4 Support

```python
config = Config()
config.connection.ipv4.enable()
config.connection.ipv4.disable()
config.connection.ipv4.isenabled  # Check status
```

### IPv6 Support

```python
config.connection.ipv6.enable()    # May raise IOError if unsupported
config.connection.ipv6.disable()
config.connection.ipv6.isenabled
```

### DNS Support

```python
config.connection.dns.enable()
config.connection.dns.disable()
config.connection.dns.isenabled
```

### Timeout

```python
config.connection.timeout = 60         # Default
config.connection.timeout = 30         # Fast networks
config.connection.timeout = 120        # Slow networks
```

### Max Connections

```python
config.connection.setmaxconnections(1000)
config.connection.max_connections = 1000
```

## Files

### 01_connection_overview.py
Demonstrates default connection settings.

```bash
python 01_connection_overview.py
```

### 02_ip_versions.py
Configure IPv4 and IPv6 support.

```bash
python 02_ip_versions.py
```

### 03_timeouts_limits.py
Set timeouts and connection limits.

```bash
python 03_timeouts_limits.py
```

## Use Cases

### Fast, Reliable Network

```python
config.connection.timeout = 30
config.connection.setmaxconnections(5000)
```

### Slow, Unreliable Network

```python
config.connection.timeout = 120
config.connection.setmaxconnections(500)
```

### IPv6-Enabled Network

```python
try:
    config.connection.ipv6.enable()
except IOError:
    print("IPv6 not supported")
```

### IP-Only Mode

```python
config.connection.dns.disable()
```

## Learning Path

1. Start with **01_connection_overview.py**
2. Try **02_ip_versions.py**
3. Study **03_timeouts_limits.py**

## Notes

- IPv4 enabled by default
- IPv6 disabled by default (requires system support)
- DNS enabled by default
- Timeout applies to all socket operations
- Semaphore manages concurrent connections

## Reference

For implementation details, see `hyproxy/conf/sock.py`
