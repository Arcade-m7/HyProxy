"""
Protocols Example 1: HTTP Protocol

HTTP/1.1 protocol for web traffic.

What is HTTP?

HTTP (Hypertext Transfer Protocol):
- Standard web protocol
- Port 80 (default)
- Text-based protocol
- Used by web browsers
- Most common proxy type

HTTP Request Flow:

    1. Client sends: GET / HTTP/1.1
    2. Proxy receives request
    3. Proxy connects to destination
    4. Destination server responds
    5. Proxy sends response to client

HTTP1O1 Class:

- Implements HTTP/1.1 protocol
- Auto-detects from first byte
- Can combine with other protocols
- Inherits from BaseProtocol

Use Cases:

- Web browser proxy
- Web application proxy
- API request proxying
- Web scraping
- Content filtering
- Anonymous browsing

Protocol Detection:

When client connects:
- First byte not 0x04 or 0x05
- Treated as HTTP
- HTTP handler takes over

Browser Configuration:

To use HTTP proxy:
1. Open browser settings
2. Find proxy settings
3. Set: 127.0.0.1:1968
4. Use for all protocols
5. Test with website

"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1


def main():
    """Create a server with HTTP protocol only."""
    
    print("""
[*] HTTP Protocol Example

HTTP/1.1 proxy for web traffic

Features:
    - Web browser support
    - Text-based protocol
    - Port 80 standard
    - Most compatible
    - Easy to configure
    """)
    
    config = Config()
    
    # Create listener with HTTP only
    listener = Asynclestener(
        name='HTTPOnlyProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config)]  # Only HTTP
    )
    
    server = Server(listener)
    
    print("[*] Starting HTTP-only proxy...")
    print("[*] Listening on 127.0.0.1:1968")
    print("[*] Protocols: HTTP/1.1 only")
    print("[*] Perfect for: Web browsing")
    print("[*] Browser configuration: 127.0.0.1:1968")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
