# Asynclestener Examples

Asynclestener is the core listening component that accepts client connections and routes them to protocol handlers.

## What is Asynclestener?

Asynclestener:
- Listens on IP:port combination
- Accepts client connections
- Auto-detects protocol from first byte
- Routes to appropriate protocol handler
- Can have multiple protocols

## API Overview

```python
listener = Asynclestener(
    name='MyListener',
    ip='127.0.0.1',
    port=1968,
    protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
)
```

## Parameters

### name
Identifier for the listener (for logging/debugging)

```python
name='HTTPProxy'
name='SOCKSProxy'
```

### ip
IP address to bind to

```python
ip='127.0.0.1'      # Localhost only
ip='0.0.0.0'        # All interfaces
ip='192.168.1.100'  # Specific interface
```

### port
Port number to listen on

```python
port=1968           # Default
port=8080           # Common HTTP
port=1080           # SOCKS standard
```

### protocols
List of protocol handlers

```python
protocols=[HTTP1O1(config)]
protocols=[SOCKS5(config)]
protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
```

## Files

### 01_basic_listener.py
Default Asynclestener with basic configuration.

```bash
python 01_basic_listener.py
```

Features:
- Single listener
- Default settings
- All protocols enabled
- Standard port

### 02_named_listeners.py
Multiple named listeners with different protocols.

```bash
python 02_named_listeners.py
```

Features:
- Named listeners (for logging)
- Different protocol combinations
- HTTPListener (HTTP only)
- SOCKSListener (SOCKS4/5 only)
- UniversalListener (all protocols)

## Listener Creation

### HTTP Only

```python
config = Config()
listener = Asynclestener(
    name='HTTPOnly',
    ip='127.0.0.1',
    port=80,
    protocols=[HTTP1O1(config)]
)
```

### SOCKS Only

```python
config = Config()
listener = Asynclestener(
    name='SOCKSOnly',
    ip='127.0.0.1',
    port=1080,
    protocols=[SOCKS5(config)]
)
```

### Universal (All Protocols)

```python
config = Config()
listener = Asynclestener(
    name='Universal',
    ip='0.0.0.0',
    port=1968,
    protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
)
```

## Protocol Detection

When client connects:

1. Client sends first byte
2. BytesParser reads first byte
3. Routes to handler:
   - 0x04 = SOCKS4
   - 0x05 = SOCKS5
   - Other = HTTP

Client doesn't know about other protocols!

## Configuration Sharing

### Separate Configs

```python
config1 = Config()
config1.auth.setusername(b'admin')

config2 = Config()
config2.auth.setusername(b'guest')

listener1 = Asynclestener(..., protocols=[HTTP1O1(config1)])
listener2 = Asynclestener(..., protocols=[HTTP1O1(config2)])
```

### Shared Config

```python
config = Config()
config.auth.setusername(b'admin')

listener1 = Asynclestener(..., protocols=[HTTP1O1(config)])
listener2 = Asynclestener(..., protocols=[SOCKS5(config)])
```

## Learning Path

1. Start with **01_basic_listener.py**
2. Study **02_named_listeners.py**

## Key Concepts

### Protocol Independence
- Protocols don't know about each other
- Auto-detection transparent to client
- Can run on same port

### Configuration Flexibility
- Shared or separate configs
- Different settings per protocol
- Different auth per listener

### Named Listeners
- Useful for logging
- Helps with debugging
- Identifies which listener processed request

## Notes

- Asynclestener does NOT run the event loop
- Must be added to Server
- Server.run() starts everything
- Multiple listeners run in parallel

## Reference

For implementation details, see `hyproxy/server/serv.py`
