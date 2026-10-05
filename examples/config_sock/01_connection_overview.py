"""
Config Socket Example 1: Connection Features Overview

Connection configuration controls socket-level behavior like timeouts,
IP version support, DNS resolution, and connection limits.

Key Features:

1. IPv4 Support
   - Enabled by default
   - Standard internet protocol
   - Can be disabled to prevent IPv4 connections

2. IPv6 Support
   - Disabled by default
   - Modern internet protocol
   - Requires OS support
   - Can be enabled if system supports it

3. DNS Support
   - Enabled by default
   - Allows proxy to resolve domain names
   - Can be disabled to force IP-only mode

4. Timeout
   - Default: 60 seconds
   - Controls how long operations wait
   - Affects connection reliability

5. Max Connections
   - Optional limit on concurrent connections
   - None = unlimited
   - Controls resource usage
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a server with default connection settings."""
    
    config = Config()
    
    # Check default connection settings
    print("[*] Default Connection Settings:")
    print(f"    IPv4 enabled: {config.connection.ipv4.isenabled}")
    print(f"    IPv6 enabled: {config.connection.ipv6.isenabled}")
    print(f"    DNS enabled: {config.connection.dns.isenabled}")
    print(f"    Timeout: {config.connection.timeout} seconds")
    print(f"    Max connections: {config.connection.max_connections}")
    print()
    
    listener = Asynclestener(
        name='DefaultSocketConfig',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("[*] Starting server with default connection configuration...")
    server.run()


if __name__ == '__main__':
    main()
