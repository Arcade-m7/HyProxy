"""
Server Example 1: Basic Server Setup

The simplest way to start a HyProxy server.

What is Server?

Server is the main entry point:
- Container for Asynclestener objects
- Starts the asyncio event loop
- Manages all listeners simultaneously
- Runs forever until interrupted (Ctrl+C)

Architecture:

    Server
        └── Asynclestener
            ├── IP: 127.0.0.1
            ├── Port: 1968
            └── Protocols:
                ├── HTTP1O1
                ├── SOCKS4
                └── SOCKS5

Flow:

    1. Create Config (optional)
    2. Create Asynclestener with protocols
    3. Create Server with listener(s)
    4. Call server.run() to start
    5. Server starts asyncio event loop
    6. All listeners accept connections
    7. Clients connect and use proxy
    8. Ctrl+C stops server

Key Points:
- One server can manage multiple listeners
- Each listener can have different protocols
- Protocols auto-detect from first byte
- Server.run() starts asyncio and blocks
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create and run a server with one listener."""
    
    print("""
[*] Basic Server Example

This example shows the simplest server setup.

Steps:
    1. Create Config (optional, can customize behavior)
    2. Create Asynclestener on port 1968
    3. Add protocols (HTTP, SOCKS4, SOCKS5)
    4. Create Server with listener
    5. Call server.run()
    """)
    
    # Step 1: Create configuration
    config = Config()
    
    # Step 2: Create a listener
    # - Listens on localhost (127.0.0.1)
    # - Listens on port 1968
    # - Supports all three protocols
    # - Named 'BasicListener' for identification
    listener = Asynclestener(
        name='BasicListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    # Step 3: Create a server and add listener
    server = Server(listener)
    
    # Step 4: Run the server
    # This starts asyncio event loop and blocks
    print("[*] Starting basic server...")
    print("[*] Listening on 127.0.0.1:1968")
    print("[*] Protocols: HTTP, SOCKS4, SOCKS5")
    print("[*] Press Ctrl+C to stop")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user")
