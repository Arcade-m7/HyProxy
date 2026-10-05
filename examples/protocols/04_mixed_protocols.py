"""
Protocols Example 4: Mixed Protocols with Auto-Detection

Support multiple protocols on a single listener.

Auto-Detection:

HyProxy examines first byte to determine protocol:

    First byte = 0x04 → SOCKS4
    First byte = 0x05 → SOCKS5
    First byte = other → HTTP

Examples:

    SOCKS4: 0x04 0x01 ... (starts with 0x04)
    SOCKS5: 0x05 0x00 ... (starts with 0x05)
    HTTP: GET / HTTP/1.1 (starts with 0x47 = 'G')

Benefits:

- One port handles all protocols
- Transparent to clients
- Clients unaware of others
- Maximum flexibility
- Simplified infrastructure

Flow:

    Client connects
        ↓
    First byte received
        ↓
    BytesParser checks first byte
        ↓
    Route to handler:
        ├─ 0x04 → SOCKS4
        ├─ 0x05 → SOCKS5
        └─ Other → HTTP
        ↓
    Protocol handler takes over
        ↓
    Full protocol negotiation

Use Cases:

1. Enterprise Proxy
   - Web browsers (HTTP)
   - VPN applications (SOCKS5)
   - Legacy applications (SOCKS4)
   - All on port 1968

2. Mixed Environment
   - Different client types
   - Different requirements
   - Single point of entry

3. Transparent Proxying
   - No client configuration
   - Automatic protocol detection
   - Works with any client
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a server supporting all protocols."""
    
    print("""
[*] Mixed Protocols Example

All protocols on one port with auto-detection.

Supported:
    - HTTP: Web browsers
    - SOCKS4: Legacy applications
    - SOCKS5: Modern VPN apps
    """)
    
    config = Config()
    
    # Create listener with all three protocols
    listener = Asynclestener(
        name='UniversalProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]  # All three!
    )
    
    server = Server(listener)
    
    print("[*] Starting universal proxy server...")
    print("[*] Listening on 127.0.0.1:1968")
    print("[*] Protocols: HTTP, SOCKS4, SOCKS5")
    print("[*] Auto-detection by first byte")
    print()
    print("[*] Clients can use any protocol:")
    print("    - Web browsers (HTTP)")
    print("    - SOCKS5 clients (VPN apps)")
    print("    - SOCKS4 clients (Legacy apps)")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
