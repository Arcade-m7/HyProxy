# Server Examples

The Server class is the main entry point for running HyProxy. It manages one or more Asynclestener objects and starts the asyncio event loop.

## What is Server?

Server is a container that:
- Holds multiple Asynclestener objects
- Starts the asyncio event loop
- Manages all listeners simultaneously
- Handles graceful shutdown

## API Overview

```python
server = Server(listener1, listener2, listener3)
server.run()
```

## Files

### 01_basic_server.py
Single listener on default port.

```bash
python 01_basic_server.py
```

Features:
- Simplest setup
- One listener
- One port (1968)
- Default configuration

### 02_multiple_listeners.py
Multiple listeners on different ports.

```bash
python 02_multiple_listeners.py
```

Features:
- Three listeners
- Ports 1968, 1969, 1970
- Same configuration
- All run simultaneously

### 03_different_ips.py
Listeners on different network interfaces.

```bash
python 03_different_ips.py
```

Features:
- Different IP bindings
- 127.0.0.1 (localhost)
- 0.0.0.0 (all interfaces)
- Different network configurations

## Server Usage

### Single Listener

```python
config = Config()
listener = Asynclestener(
    name='MyProxy',
    ip='127.0.0.1',
    port=1968,
    protocols=[HTTP1O1(config), SOCKS5(config)]
)

server = Server(listener)
server.run()
```

### Multiple Listeners

```python
config1 = Config()
listener1 = Asynclestener(
    name='Listener1',
    ip='127.0.0.1',
    port=1968,
    protocols=[HTTP1O1(config1), SOCKS5(config1)]
)

config2 = Config()
listener2 = Asynclestener(
    name='Listener2',
    ip='0.0.0.0',
    port=8080,
    protocols=[HTTP1O1(config2)]
)

server = Server(listener1, listener2)
server.run()
```

## Key Concepts

### Event Loop
- Server starts asyncio event loop
- All listeners run concurrently
- Loop continues until interrupted

### Multiple Listeners
- Each listener on own port/IP
- Independent configurations
- Shared or separate configs

### Graceful Shutdown
- Ctrl+C stops event loop
- All connections closed cleanly
- Resources released

## Learning Path

1. Start with **01_basic_server.py**
2. Try **02_multiple_listeners.py**
3. Study **03_different_ips.py**

## Notes

- Server runs forever until interrupted
- Use Ctrl+C to stop
- All listeners start immediately
- Listeners run in parallel

## Reference

For implementation details, see `hyproxy/server/serv.py`
