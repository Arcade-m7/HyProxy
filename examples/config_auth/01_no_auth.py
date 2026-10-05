"""
Config Auth Example 1: No Authentication

No authentication required - allow all connections.

Default Behavior:

By default, HyProxy requires no credentials.
Clients can connect and use proxy immediately.

Authentication Flow (No Auth):

    Client connects
        ↓
    Request sent (no credentials needed)
        ↓
    Proxy processes request
        ↓
    Response sent to client
    ✓ No auth check!

When to Use:

- Public proxy servers
- Testing and development environments
- Internal corporate networks (trusted)
- Prototype deployments
- Performance testing

Security Implications:

- Anyone with access can use proxy
- No access control
- Not recommended for production

Alternatives:

- Single auth (01_basic_auth.py)
- Multiple users (03_multiple_credentials.py)
- Combine with IP policies
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a server without authentication."""
    
    print("""
[*] No Authentication Example

Default behavior: Allow all connections

No credentials required:
    - Fastest performance
    - Easiest setup
    - No security
    - Best for testing
    """)
    
    # Create config (no auth needed)
    config = Config()
    
    # Important: Don't set any auth credentials
    # config.auth.setusername(...) - NOT called
    # config.auth.setpassword(...) - NOT called
    # This means auth is disabled (default)
    
    listener = Asynclestener(
        name='NoAuthListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("[*] Starting server...")
    print("[*] Authentication: DISABLED")
    print("[*] Clients can connect without credentials")
    print("[*] All connections allowed")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
