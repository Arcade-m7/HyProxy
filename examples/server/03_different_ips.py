"""
Server Example 3: Listeners on Different Network Interfaces

Bind listeners to different IP addresses for various network scenarios.

Network Binding Options:

'0.0.0.0'
- Listen on ALL network interfaces
- Accessible from any machine
- Requires firewall rules
- Good for: Shared proxies, servers

'127.0.0.1'
- Localhost only
- Only accessible from this machine
- Cannot access from other machines
- Good for: Development, local testing

'192.168.1.100' (or any specific IP)
- Listen on one interface only
- Only accessible on that network
- Good for: Multi-homed servers
- Requires actual IP to exist

'::1'
- IPv6 localhost
- Requires IPv6 support
- Only local access

'::'
- IPv6 all interfaces
- Requires IPv6 support
- Accessible from any machine

Use Cases:

1. Public Proxy Server
   IP: 0.0.0.0
   Port: 1968
   Accessible: Anywhere on internet

2. Development Machine
   IP: 127.0.0.1
   Port: 1968
   Accessible: Only locally

3. Corporate Proxy
   IP: 192.168.1.100
   Port: 1968
   Accessible: Only on corporate network

Security Implications:

- 0.0.0.0: Requires strong auth, firewall
- 127.0.0.1: Safe, no external access
- Specific IP: Medium security
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create listeners on different network interfaces."""
    
    print("""
[*] Different Network Interfaces Example

Three listeners on different IP bindings.

Setup:
    Port 1968: All interfaces (0.0.0.0)
    Port 1969: Localhost only (127.0.0.1)
    Port 1970: Specific interface (127.0.0.1)
    """)
    
    config = Config()
    
    # Listener on all interfaces (accessible from anywhere)
    listener_all = Asynclestener(
        name='AllInterfaces',
        ip='0.0.0.0',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    # Listener on localhost (only local access)
    listener_localhost = Asynclestener(
        name='LocalhostOnly',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    # Listener on localhost (another port)
    listener_local_alt = Asynclestener(
        name='LocalhostAlt',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config), SOCKS5(config)]
    )
    
    server = Server(listener_all, listener_localhost, listener_local_alt)
    
    print("[*] Starting server with different network bindings...")
    print("[*] AllInterfaces: 0.0.0.0:1968 (Accessible from anywhere)")
    print("[*] LocalhostOnly: 127.0.0.1:1969 (Local only)")
    print("[*] LocalhostAlt: 127.0.0.1:1970 (Local only)")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
