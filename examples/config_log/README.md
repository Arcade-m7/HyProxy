# Config LOG Examples

This folder contains examples demonstrating the LOG (Logging) configuration in HyProxy.

## What is LOG?

LOG controls connection logging and debugging information. HyProxy uses Python's logging module with custom handlers.

### Key Components

1. **__log__** Class
   - Custom logger inheriting from logging.Logger
   - Formats messages with timestamp and level
   - Default name: "NETWORK"
   - Default logging level: DEBUG

2. **StreamOutput** Class
   - Custom logging handler
   - Formats each log entry as: `timestamp | level | message`
   - Attached to logger by default
   - Can be enabled/disabled dynamically

3. **Connection Logging**
   - Records detailed connection information
   - Includes protocol, listener name, UUID, timing
   - Tracks source/destination, bytes transferred
   - Captures any errors

## API Overview

### Accessing the Logger

```python
config = Config()
config.log  # The logger instance
```

### Controlling Stream Output

```python
# Enable logging (attach handler to logger)
config.log.stream.enable()

# Disable logging (remove handler from logger)
config.log.stream.disable()

# Reinitialize with new stream
config.log.stream.reinit(stream=new_stream_object)
```

### Log Message Format

Each log entry contains:
```
timestamp | level | message
```

Example:
```
2026-07-03 14:30:45,123 | DEBUG | [SOCKS5]:[ProxyListener] UUID=abc123, STIME=12:34:56, ETIME=12:35:10, SRCADDR=192.168.1.100:56789, DSTADDR=8.8.8.8:53, DATASENT=1024, DATARECV=2048, error=None
```

### Connection Information Fields

- **protocol**: HTTP1O1, SOCKS4, or SOCKS5
- **lname**: Listener name
- **uuid**: Unique connection identifier
- **stime**: Connection start time
- **etime**: Connection end time
- **srcaddr**: Source address (client IP:port)
- **dstaddr**: Destination address (target IP:port)
- **datas**: Data sent (bytes)
- **datar**: Data received (bytes)
- **error**: Error message (if any)

## Files

### 01_basic_logging.py
Shows logging enabled by default and explains the logging system.

```bash
python 01_basic_logging.py
```

### 02_logging_control.py
Demonstrates enabling/disabling logging on different listeners.

Scenarios:
- Production: Logging enabled for auditing
- Development: Detailed logging for debugging
- High-performance: Logging disabled for throughput

```bash
python 02_logging_control.py
```

### 03_custom_streams.py
Explains advanced logging with different output streams.

```bash
python 03_custom_streams.py
```

## Use Cases

### Production Logging

```python
# Production: Keep all logs
prod_config = Config()
# Logging enabled by default
prod_listener = Asynclestener(
    name='ProdProxy',
    ip='0.0.0.0',
    port=1968,
    protocols=[HTTP1O1(prod_config), SOCKS5(prod_config)]
)
```

### Performance Optimization

```python
# High-traffic: Disable logging for better throughput
perf_config = Config()
perf_config.log.stream.desible()  # Disable stream output
```

### Selective Logging

```python
# Log monitoring
config = Config()
# Logging enabled by default
# Later can disable with:
# config.log.stream.desible()
```

## Learning Path

1. Start with **01_basic_logging.py** - Understand logging format
2. Try **02_logging_control.py** - See enable/disable
3. Study **03_custom_streams.py** - Learn about stream options

## Log Levels

HyProxy uses Python's standard logging levels:
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages for potential issues
- ERROR: Error messages for problems

## Stream Types

```python
import sys
import io

# Standard output (default)
config.log.stream.reinit(stream=sys.stdout)

# Standard error
config.log.stream.reinit(stream=sys.stderr)

# File
config.log.stream.reinit(stream=open('proxy.log', 'a'))

# In-memory buffer
buffer = io.StringIO()
config.log.stream.reinit(stream=buffer)
```

## Performance Considerations

- Logging adds overhead
- Disable for maximum throughput
- Enable for production auditing
- Use in development for debugging

## Viewing Logs

Logs are written to the stream (usually stdout):

```
[SOCKS5]:[MainProxy] UUID=550e8400-e29b-41d4-a716-446655440000
  Connection: 192.168.1.50:54321 -> 8.8.8.8:53
  Data: Sent 512 bytes, Received 1024 bytes
  Time: 0.234 seconds
```

## Notes

- Logging is enabled by default
- Each connection gets a unique UUID
- Full connection lifecycle is logged
- Multiple listeners can have different logging states

## Advanced Topics

See also:
- `config_cmd/` for command logging
- `config_policy/` for policy logging
- `config_auth/` for authentication logs

## Reference

For implementation details, see:
- `hyproxy/conf/log.py` - Logging implementation
- `hyproxy/net/const.py` - CONNECTIONINFO dataclass
