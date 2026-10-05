# DNS Utilities Examples

DNS resolution with automatic caching system.

## What is DNS Caching?

Automatic caching of DNS lookups to:
- Reduce network traffic
- Improve performance
- Speed up repeated lookups
- Reduce latency

## Key Features

- Separate IPv4 (type A) and IPv6 (type AAAA) caches
- 3-minute TTL (Time To Live) by default
- Thread-safe with asyncio locks
- Multiple nameservers
- Automatic fallback between servers

## API Overview

### Basic Resolution

```python
from hyproxy.utills.dns import DNS

# Resolve IPv4
ip = await DNS.resolve('example.com', 'A')

# Resolve IPv6
ip = await DNS.resolve('example.com', 'AAAA')
```

### Configuration

```python
# Change nameservers
DNS.nameservers = ['8.8.8.8', '1.1.1.1']

# Change cache TTL
DNS.TTL = 300  # 5 minutes
```

### Cache Access

```python
# IPv4 cache
DNS.cache.ipv4['example.com']  # CACHE object

# IPv6 cache
DNS.cache.ipv6['example.com']  # CACHE object

# Cache size
len(DNS.cache.ipv4)
len(DNS.cache.ipv6)
```

## Files

### 01_dns_caching.py
Overview of DNS caching system.

```bash
python 01_dns_caching.py
```

Topics:
- Caching mechanism
- Cache benefits
- TTL configuration
- Nameserver options

### 02_query_types.py
IPv4 and IPv6 query types.

```bash
python 02_query_types.py
```

Topics:
- Type A (IPv4) queries
- Type AAAA (IPv6) queries
- Address formats
- Resolution flow

### 03_advanced_config.py
Advanced DNS configurations.

```bash
python 03_advanced_config.py
```

Scenarios:
- Internal network DNS
- Privacy-focused DNS
- Performance-optimized DNS

## DNS Query Types

### Type 'A' - IPv4

```python
# Query example.com for IPv4
ip = await DNS.resolve('example.com', 'A')
# Returns: '93.184.216.34'
```

### Type 'AAAA' - IPv6

```python
# Query example.com for IPv6
ip = await DNS.resolve('example.com', 'AAAA')
# Returns: '2606:2800:220:1:248:1893:25c8:1946'
```

## Performance Impact

### First Query (Cache Miss)
```
Time: 50-200ms
Operations:
  1. Query nameserver
  2. Wait for response
  3. Parse response
  4. Store in cache
  5. Return result
```

### Subsequent Queries (Cache Hit)
```
Time: <1ms
Operations:
  1. Look up in cache
  2. Check expiration
  3. Return cached result
```

## Customization Patterns

### Internal Network

```python
DNS.nameservers = ['192.168.1.1', '192.168.1.2']
DNS.TTL = 300  # 5 minutes
```

### Privacy-Focused

```python
DNS.nameservers = ['1.1.1.1', '9.9.9.9']
DNS.TTL = 180  # 3 minutes
```

### High Performance

```python
DNS.nameservers = ['8.8.8.8', '8.8.4.4']
DNS.TTL = 3600  # 1 hour
```

## Common Nameservers

### Public DNS Servers

| Provider | IPv4 | Type |
|----------|------|------|
| Google | 8.8.8.8 | Public |
| Cloudflare | 1.1.1.1 | Privacy |
| Quad9 | 9.9.9.9 | Security |
| OpenDNS | 208.67.222.222 | Content filter |

## Learning Path

1. Start with **01_dns_caching.py**
2. Study **02_query_types.py**
3. Explore **03_advanced_config.py**

## Cache DATACLASS

```python
@dataclass
class CACHE:
    ip: str              # Resolved IP address
    timeex: float|int    # Expiration time
```

## Error Handling

Returns `None` when:
- Domain doesn't exist
- DNS server unreachable
- Query timeout
- Invalid query type
- No IPv6 support (for AAAA)

## Thread Safety

All operations are thread-safe thanks to:
```python
lock = asyncio.Lock()  # Prevents race conditions
```

## Reference

For implementation details, see `hyproxy/utills/dns.py`
