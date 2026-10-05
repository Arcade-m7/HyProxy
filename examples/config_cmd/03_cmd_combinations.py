"""
Config CMD Example 3: Advanced Command Combinations

You can mix authentication with command control for fine-grained access policies.

Use Cases:
- Admin users: All commands enabled
- Standard users: Limited commands (no BIND)
- Guest users: Only CONNECT allowed
- Read-only: No CONNECT allowed

This allows different security levels per listener.
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def admin_listener():
    """Create admin listener with all commands enabled."""
    config = Config()
    config.auth.setusername(b'admin')
    config.auth.setpassword(b'admin')
    # All commands enabled by default
    
    return Asynclestener(
        name='AdminListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )


def user_listener():
    """Create user listener with limited commands."""
    config = Config()
    config.auth.setusername(b'user')
    config.auth.setpassword(b'user')
    # Disable BIND (no reverse connections)
    config.cmd.bind.desible()
    # Disable UDP (no UDP traffic)
    config.cmd.udp.desible()
    
    return Asynclestener(
        name='UserListener',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )


def guest_listener():
    """Create guest listener with minimal commands."""
    config = Config()
    config.auth.setusername(b'guest')
    config.auth.setpassword(b'guest')
    # Disable BIND and UDP for guest
    config.cmd.bind.desible()
    config.cmd.udp.desible()
    
    return Asynclestener(
        name='GuestListener',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config), SOCKS5(config)]
    )


def print_commands(config, name):
    """Print command status for a config."""
    print(f"[*] {name}:")
    print(f"    CONNECT (1): {config.cmd.get(1)}")
    print(f"    BIND (2):    {config.cmd.get(2)}")
    print(f"    UDP (3):     {config.cmd.get(3)}")


def main():
    """Create multiple listeners with different command access levels."""
    
    admin = admin_listener()
    user = user_listener()
    guest = guest_listener()
    
    server = Server(admin, user, guest)
    
    print("[*] Starting server with command-based access control...")
    print()
    
    print_commands(admin.protocols[0].config, "Admin (port 1968)")
    print_commands(user.protocols[0].config, "User (port 1969)")
    print_commands(guest.protocols[0].config, "Guest (port 1970)")
    print()
    
    server.run()


if __name__ == '__main__':
    main()
