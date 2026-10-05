"""
Protocols Example 3: SOCKS5 Protocol

SOCKS5 is the modern SOCKS protocol.

What is SOCKS5?
- Modern version of SOCKS protocol
- Supports any TCP/UDP traffic
- Port: Typically 1080
- Full authentication support (username/password)
- IPv6 support
- More features than SOCKS4
- More secure than SOCKS4

SOCKS5 in HyProxy:
- Implements full SOCKS5 protocol
- Can be instantiated with or without Config
- Supports authentication if Config is provided
- Most commonly used SOCKS protocol

Use cases:
- Modern SOCKS applications
- VPN-like functionality
- Full TCP traffic proxying
- Applications requiring authentication

Advantages over SOCKS4:
- IPv6 support
- Authentication support
- Better error handling
- More protocol flexibility
"""

from hyproxy import Server, Asynclestener
from hyproxy.protocols import SOCKS5


def main():
    """Create a server with SOCKS5 protocol only."""
    
    # Create listener with SOCKS5 only
    listener = Asynclestener(
        name='SOCKS5OnlyProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[SOCKS5()]  # Only SOCKS5
    )
    
    server = Server(listener)
    
    print("[*] Starting SOCKS5-only proxy server...")
    print("[*] Supports: SOCKS5 protocol")
    print("[*] Features: IPv6, authentication, UDP support")
    print("[*] Perfect for: Modern applications and VPN-like usage")
    print("[*] Standard SOCKS5 port: 1080")
    print()
    server.run()


if __name__ == '__main__':
    main()
