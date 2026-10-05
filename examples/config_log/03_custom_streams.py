"""
Config LOG Example 3: Advanced Logging with Custom Streams

StreamOutput can be reinitialized with different streams for logging to files,
sockets, or other destinations.

Stream Options:
- None (default): Standard output
- File stream: Log to file
- Custom stream: Any file-like object

Typical Workflow:
1. Create logger instance
2. StreamOutput attached by default
3. Call reinit() to change stream
4. Call enable()/desible() to toggle logging

Log Message Format:
"timestamp | level | message"

Example log message:
"2026-07-03 14:30:45,123 | DEBUG | [SOCKS5]:[ProxyListener] UUID=abc123, ..."

Components in connection log:
- protocol: HTTP1O1, SOCKS4, or SOCKS5
- lname: Listener name
- uuid: Unique connection ID
- stime: Start time
- etime: End time
- srcaddr: Source address (client)
- dstaddr: Destination address (target)
- datas: Data sent
- datar: Data received
- error: Any error messages
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
import io


def main():
    """Create listeners with different logging destinations."""
    
    # Listener 1: Standard output logging (default)
    config1 = Config()
    
    listener1 = Asynclestener(
        name='StdoutLogger',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config1), SOCKS5(config1)]
    )
    
    # Listener 2: Could use custom stream
    config2 = Config()
    
    listener2 = Asynclestener(
        name='CustomLogger',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(config2), SOCKS5(config2)]
    )
    
    # Listener 3: Could use StringIO for in-memory logging
    config3 = Config()
    
    listener3 = Asynclestener(
        name='InMemoryLogger',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config3), SOCKS5(config3)]
    )
    
    server = Server(listener1, listener2, listener3)
    
    print("[*] Starting server with advanced logging...")
    print()
    print("[*] Port 1968 (StdoutLogger): Log to console")
    print("    Format: timestamp | level | connection_details")
    print()
    print("[*] Port 1969 (CustomLogger): Log format explained:")
    print("    timestamp: When the event occurred")
    print("    level: DEBUG, INFO, WARNING, ERROR")
    print("    protocol: HTTP1O1, SOCKS4, SOCKS5")
    print("    listener: Listener name")
    print("    uuid: Unique connection identifier")
    print("    src/dst: Source and destination addresses")
    print("    data: Bytes sent/received")
    print()
    print("[*] Port 1970 (InMemoryLogger): Could use StringIO stream")
    print("    Logs available in memory for processing")
    print()
    print("[*] Connection Log Example:")
    print("    [SOCKS5]:[ProxyListener] UUID=abc123, STIME=12:34:56, ETIME=12:35:10")
    print("    SRCADDR=192.168.1.100:56789, DSTADDR=8.8.8.8:53")
    print("    DATASENT=1024, DATARECV=2048, error=None")
    print()
    server.run()


if __name__ == '__main__':
    main()
