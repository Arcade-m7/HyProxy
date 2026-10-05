"""
Asynclestener Example 2: Named Listeners with Specific Protocols

Customize listener names and protocol support.

Listener Naming:

- Identifies listener in logs
- Useful for multiple listeners
- Helps with debugging
- Shows which listener handled connection

Protocol Selection:

Instead of supporting all protocols:
- Choose only what clients need
- Reduces complexity
- Improves performance
- Simplifies security

Common Patterns:

1. HTTP Only Listener
   - For web browsers
   - Port 80 or 8080
   - Lightweight

2. SOCKS Only Listener
   - For VPN/SOCKS clients
   - Port 1080
   - Clients choose SOCKS4/5

3. All Protocols
   - Maximum compatibility
   - Auto-detection
   - Default setup

Benefits of Specialization:

- Dedicated resources
- Specific security policies
- Different auth per listener
- Granular control

Example Scenario:

    Port 1968: Public HTTP proxy
    Port 1069: Internal SOCKS proxy  
    Port 8080: Admin access (all protocols)
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create named listeners with specific protocol support."""
    
    print("""
[*] Named Listeners Example

Three specialized listeners on different ports.

Setup:
    Port 1968: HTTP only
    Port 1969: SOCKS only
    Port 1970: All protocols
    """)
    
    config = Config()
    
    # HTTP-only listener (lightweight, simple)
    http_listener = Asynclestener(
        name='HTTPListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config)]
    )
    
    # SOCKS4 + SOCKS5 listener (for SOCKS clients)
    socks_listener = Asynclestener(
        name='SOCKSListener',
        ip='127.0.0.1',
        port=1969,
        protocols=[SOCKS4(config), SOCKS5(config)]
    )
    
    # All protocols listener (full compatibility)
    full_listener = Asynclestener(
        name='UniversalListener',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(http_listener, socks_listener, full_listener)
    
    print("[*] Starting named listeners...")
    print("[*] HTTPListener: 127.0.0.1:1968 (HTTP only)")
    print("[*] SOCKSListener: 127.0.0.1:1969 (SOCKS4 + SOCKS5)")
    print("[*] UniversalListener: 127.0.0.1:1970 (All protocols)")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
