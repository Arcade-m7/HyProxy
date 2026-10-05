"""
Protocols Example 2: SOCKS4 Protocol

SOCKS4 is an older SOCKS protocol.

What is SOCKS4?
- SOCKS stands for Socket Secure
- Protocol for proxying any TCP traffic (not just HTTP)
- Port: Typically 1080
- Simpler than SOCKS5 but less feature-rich
- Limited support for authentication
- No support for IPv6

SOCKS4 in HyProxy:
- Implements SOCKS4 protocol
- Can be instantiated with or without Config
- Good for legacy applications

Use cases:
- Legacy applications that require SOCKS4
- Simple TCP proxying
- Applications that don't support SOCKS5

Note: SOCKS4a is an extension that supports domain names (not just IPs)
"""

from hyproxy import Server, Asynclestener
from hyproxy.protocols import SOCKS4


def main():
    """Create a server with SOCKS4 protocol only."""
    
    # Create listener with SOCKS4 only
    listener = Asynclestener(
        name='SOCKS4OnlyProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[SOCKS4()]  # Only SOCKS4
    )
    
    server = Server(listener)
    
    print("[*] Starting SOCKS4-only proxy server...")
    print("[*] Supports: SOCKS4 protocol")
    print("[*] Perfect for: Legacy applications and simple TCP proxying")
    print("[*] Standard SOCKS4 port: 1080")
    print()
    server.run()


if __name__ == '__main__':
    main()
