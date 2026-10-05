"""
Config LOG Example 1: Understanding Logging

HyProxy uses Python's logging module with custom handlers.

Key Components:

1. __log__ class
   - Custom logger inheriting from logging.Logger
   - Formats log messages with timestamp and level
   - Default name: "NETWORK"
   - Default level: logging.DEBUG

2. StreamOutput class
   - Custom logging handler
   - Formats messages as: "timestamp | level | message"
   - Can be enabled/disabled dynamically
   - Can be initialized with custom stream

3. Logging Operations:
   - stream.enable() - Start logging to stream
   - stream.desible() - Stop logging to stream
   - stream.reinit() - Reinitialize with new stream

4. Connection Information Logging:
   - Protocol used
   - Listener name
   - UUID for connection
   - Start and end times
   - Source and destination addresses
   - Data sent and received
   - Any errors that occurred
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a server with logging enabled."""
    
    config = Config()
    
    # Logging is enabled by default in HyProxy
    # All connections will be logged with: timestamp, level, message
    
    listener = Asynclestener(
        name='LoggingEnabledListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("[*] Starting server with logging enabled...")
    print("[*] Format: timestamp | level | protocol:[listener] | connection details")
    print("[*] Each connection will be logged with UUID, addresses, and data transferred")
    print()
    server.run()


if __name__ == '__main__':
    main()

