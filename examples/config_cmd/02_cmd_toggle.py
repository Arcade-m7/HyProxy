"""
Config CMD Example 2: Controlling Specific Commands

Each command can be individually controlled with enable() and desible() methods.

Command IDs:
- 1: CONNECT - Establish connections
- 2: BIND - Bind to ports (reverse connections)
- 3: UDP - UDP protocol support

Methods:
- config.cmd.connect.enable() - Enable CONNECT
- config.cmd.connect.desible() - Disable CONNECT (note: typo in source)
- config.cmd.get(1) - Check if CONNECT is enabled

Similarly for bind and udp:
- config.cmd.bind.enable() / .desible()
- config.cmd.udp.enable() / .desible()
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create configs with different command configurations."""
    
    # Config 1: Disable UDP command (no UDP support)
    config1 = Config()
    config1.cmd.udp.desible()  # Disable UDP
    
    listener1 = Asynclestener(
        name='NoUDPListener',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config1), SOCKS5(config1)]
    )
    
    # Config 2: Disable BIND command (no reverse connections)
    config2 = Config()
    config2.cmd.bind.desible()  # Disable BIND
    
    listener2 = Asynclestener(
        name='NoBindListener',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(config2), SOCKS5(config2)]
    )
    
    # Config 3: Disable CONNECT command (no outgoing connections)
    config3 = Config()
    config3.cmd.connect.desible()  # Disable CONNECT
    
    listener3 = Asynclestener(
        name='NoConnectListener',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(config3), SOCKS5(config3)]
    )
    
    server = Server(listener1, listener2, listener3)
    
    print("[*] Starting server with selective command support...")
    print()
    print("[*] Port 1968 (NoUDPListener):")
    print(f"    CONNECT: {listener1.protocols[0].config.cmd.get(1)}")
    print(f"    BIND:    {listener1.protocols[0].config.cmd.get(2)}")
    print(f"    UDP:     {listener1.protocols[0].config.cmd.get(3)}")
    print()
    print("[*] Port 1969 (NoBindListener):")
    print(f"    CONNECT: {listener2.protocols[0].config.cmd.get(1)}")
    print(f"    BIND:    {listener2.protocols[0].config.cmd.get(2)}")
    print(f"    UDP:     {listener2.protocols[0].config.cmd.get(3)}")
    print()
    print("[*] Port 1970 (NoConnectListener):")
    print(f"    CONNECT: {listener3.protocols[0].config.cmd.get(1)}")
    print(f"    BIND:    {listener3.protocols[0].config.cmd.get(2)}")
    print(f"    UDP:     {listener3.protocols[0].config.cmd.get(3)}")
    print()
    server.run()


if __name__ == '__main__':
    main()
