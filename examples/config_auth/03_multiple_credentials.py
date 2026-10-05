"""
Config Auth Example 3: Multiple Listeners with Different Credentials

Different users on different ports with different access levels.

Multi-Tier Access Pattern:

    Admin Tier:
    - Username: admin
    - Password: complex_password
    - Full access
    
    User Tier:
    - Username: user
    - Password: standard_password
    - Standard access
    
    Guest Tier:
    - Username: guest
    - Password: simple_password
    - Limited access

Benefits:

- Separate access levels
- Different auth per port
- Can apply different policies per port
- User tracking and auditing
- Granular permission control

Implementation:

For each tier:
1. Create separate Config
2. Set unique credentials
3. Create listener with Config
4. Add to Server

Combined with Policies:

    Admin tier:
    - Access all ports
    - Full bandwidth
    
    User tier:
    - Web only (ports 80, 443)
    - Standard bandwidth
    
    Guest tier:
    - Limited ports only
    - Restricted bandwidth

Production Recommendation:

- Use strong passwords for each tier
- Store credentials in environment variables
- Apply different policies per tier
- Monitor access per tier
- Log authentication failures
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create multiple listeners with different credentials."""
    
    print("""
[*] Multiple Credentials Example

Three listeners with different access tiers.

Setup:
    Port 1968: Admin (full access)
    Port 1969: User (standard access)
    Port 1970: Guest (limited access)
    """)
    
    # Admin tier config
    admin_config = Config()
    admin_config.auth.setusername(b'admin')
    admin_config.auth.setpassword(b'admin_secure_pass')
    
    admin_listener = Asynclestener(
        name='AdminListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(admin_config), SOCKS4(admin_config), SOCKS5(admin_config)]
    )
    
    # User tier config
    user_config = Config()
    user_config.auth.setusername(b'user')
    user_config.auth.setpassword(b'user_password')
    
    user_listener = Asynclestener(
        name='UserListener',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(user_config), SOCKS4(user_config), SOCKS5(user_config)]
    )
    
    # Guest tier config
    guest_config = Config()
    guest_config.auth.setusername(b'guest')
    guest_config.auth.setpassword(b'guest123')
    
    guest_listener = Asynclestener(
        name='GuestListener',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(guest_config)]  # HTTP only for guests
    )
    
    server = Server(admin_listener, user_listener, guest_listener)
    
    print("[*] Starting multi-tier proxy...")
    print("[*] AdminListener: 127.0.0.1:1968 (admin / admin_secure_pass)")
    print("[*] UserListener: 127.0.0.1:1969 (user / user_password)")
    print("[*] GuestListener: 127.0.0.1:1970 (guest / guest123)")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
