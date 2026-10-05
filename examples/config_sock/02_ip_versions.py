"""
Config Socket Example 2: IP Version Support

Control IPv4 and IPv6 support on the proxy.

IPv4:
- Internet Protocol version 4
- Default: Enabled
- 32-bit addresses (e.g., 192.168.1.1)
- Widely supported

IPv6:
- Internet Protocol version 6
- Default: Disabled
- 128-bit addresses (e.g., 2001:db8::1)
- Requires OS support
- Raises IOError if OS doesn't support it
- Can check with socket.has_ipv6

Methods:
- .enable() - Turn on
- .disable() - Turn off
- .isenabled - Check status
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5


def ipv4_only_config():
    """Config with IPv4 only (IPv6 disabled)."""
    config = Config()
    # IPv4 enabled by default
    # IPv6 disabled by default
    return config


def ipv6_enabled_config():
    """Config with IPv6 enabled if system supports it."""
    config = Config()
    try:
        config.connection.ipv6.enable()
    except IOError as e:
        print(f"[!] Warning: {e}")
    return config


def main():
    """Create listeners with different IP version support."""
    
    # IPv4-only listener
    ipv4_config = ipv4_only_config()
    ipv4_listener = Asynclestener(
        name='IPv4OnlyProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(ipv4_config), SOCKS5(ipv4_config)]
    )
    
    # IPv4 + IPv6 listener
    ipv6_config = ipv6_enabled_config()
    ipv6_listener = Asynclestener(
        name='DualStackProxy',
        ip='::',
        port=1969,
        protocols=[HTTP1O1(ipv6_config), SOCKS5(ipv6_config)]
    )
    
    server = Server(ipv4_listener, ipv6_listener)
    
    print("[*] Starting server with IP version configuration...")
    print()
    print("[*] Port 1968 (IPv4 Only):")
    print(f"    IPv4: {ipv4_listener.protocols[0].config.connection.ipv4.isenabled}")
    print(f"    IPv6: {ipv4_listener.protocols[0].config.connection.ipv6.isenabled}")
    print()
    print("[*] Port 1969 (Dual Stack):")
    print(f"    IPv4: {ipv6_listener.protocols[0].config.connection.ipv4.isenabled}")
    print(f"    IPv6: {ipv6_listener.protocols[0].config.connection.ipv6.isenabled}")
    print()
    server.run()


if __name__ == '__main__':
    main()
