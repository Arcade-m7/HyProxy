"""
Config CMD Example 1: Understanding Commands

The CMD configuration in HyProxy controls three specific commands:

1. CONNECT Command (option 1)
   - Allows clients to establish connections
   - Essential for SOCKS protocol operation
   - Default: Enabled

2. BIND Command (option 2)
   - Allows clients to bind to ports
   - Used in SOCKS protocol for reverse connections
   - Default: Enabled

3. UDP Command (option 3)
   - Enables UDP protocol support
   - Used for UDP-based communication
   - Default: Enabled

Each command can be individually enabled or disabled.
By default, all commands are enabled when Config is created.
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create a config with default command settings."""
    
    config = Config()
    
    # Check default command states (all enabled by default)
    print("[*] Default command states:")
    print(f"    CONNECT (1): {config.cmd.get(1)}")
    print(f"    BIND (2): {config.cmd.get(2)}")
    print(f"    UDP (3): {config.cmd.get(3)}")
    print()
    
    listener = Asynclestener(
        name='DefaultCmdListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("[*] Starting server with default command configuration...")
    print("[*] All commands enabled: CONNECT, BIND, UDP")
    print()
    server.run()


if __name__ == '__main__':
    main()
