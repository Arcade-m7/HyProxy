"""
Server Example 2: Multiple Listeners

A single Server can manage multiple Asynclestener objects on different ports.

Why Multiple Listeners?

- Different ports for different purposes
- Load distribution
- Protocol separation
- Redundancy and failover
- Isolated configurations

Architecture:

    Server
        ├── Listener 1 (port 1968, all protocols)
        ├── Listener 2 (port 1969, all protocols)
        └── Listener 3 (port 1970, HTTP only)

All listeners run simultaneously in same server.

Flow:

    1. Create Config
    2. Create Listener 1 on port 1968
    3. Create Listener 2 on port 1969
    4. Create Listener 3 on port 1970
    5. Create Server with all three
    6. Call server.run()
    7. All accept connections simultaneously
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create and run a server with multiple listeners."""
    
    print("""
[*] Multiple Listeners Example

One Server managing three listeners on different ports.

Setup:
    Listener 1: All protocols on port 1968
    Listener 2: All protocols on port 1969
    Listener 3: HTTP only on port 1970
    """)
    
    config = Config()
    
    # Listener 1: Port 1968
    listener1 = Asynclestener(
        name='PrimaryListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    # Listener 2: Port 1969
    listener2 = Asynclestener(
        name='SecondaryListener',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    # Listener 3: Port 1970 (HTTP only)
    listener3 = Asynclestener(
        name='HTTPOnlyListener',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config)]
    )
    
    # Create server with all listeners
    server = Server(listener1, listener2, listener3)
    
    print("[*] Starting server with multiple listeners...")
    print("[*] Listener 1: 127.0.0.1:1968 (HTTP + SOCKS4 + SOCKS5)")
    print("[*] Listener 2: 127.0.0.1:1969 (HTTP + SOCKS4 + SOCKS5)")
    print("[*] Listener 3: 127.0.0.1:1970 (HTTP only)")
    print("[*] All listening simultaneously")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
