"""
Config Auth Example 2: Single Username and Password

Require authentication with a single username/password pair.

Authentication Setup:

    config.auth.setusername(b'username')
    config.auth.setpassword(b'password')

All clients must provide these exact credentials.

Authentication Flow:

    Client connects
        ↓
    Client sends request with credentials
        ↓
    Proxy checks username
        ↓
    Proxy checks password
        ↓
    Credentials match?
        ├─ YES: Allow
        └─ NO: Deny

When to Use:

- Small deployments (1-5 users)
- Shared proxy between team members
- All users same access level
- Simple security requirement

Security Considerations:

- Single password for all users
- No individual user tracking
- No per-user access control

Production Recommendation:

- Use environment variables for password
- Use strong passwords (16+ characters)
- Change password regularly
- Monitor access logs
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a server with basic authentication."""
    
    print("""
[*] Basic Authentication Example

Single username and password for all users.

Setup:
    Username: admin
    Password: secret123
    """)
    
    config = Config()
    
    # Set single authentication credentials (as bytes)
    config.auth.setusername(b'admin')
    config.auth.setpassword(b'secret123')
    
    listener = Asynclestener(
        name='AuthListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("[*] Starting server...")
    print("[*] Authentication: ENABLED")
    print("[*] Username: admin")
    print("[*] Password: secret123")
    print("[*] Clients must provide correct credentials")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
