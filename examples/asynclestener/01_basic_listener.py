"""
Asynclestener Example 1: Basic Listener

The simplest possible listener setup.

What is Asynclestener?

Asynclestener:
- Listens on IP:port combination
- Accepts incoming client connections
- Auto-detects protocol (HTTP, SOCKS4, SOCKS5)
- Routes each connection to appropriate handler
- Handles many connections asynchronously

Parameters:

- name: Identifier for logs/debugging
- ip: IP address to bind to
  - '0.0.0.0' = all interfaces (default)
  - '127.0.0.1' = localhost only
  - '192.168.x.x' = specific interface
- port: Port number (default 1968)
- protocols: List of protocol handlers

Default Behavior:

If you only specify port:
- IP: 0.0.0.0 (all interfaces)
- Protocols: HTTP, SOCKS4, SOCKS5 (all three)
- Name: Auto-generated

Minimal Setup:

    listener = Asynclestener(port=1968)

This is the simplest possible configuration!

Flow:

    1. Create Asynclestener
    2. Bind to IP:port
    3. Wait for client connections
    4. Client connects
    5. Read first byte
    6. Determine protocol
    7. Route to handler
    8. Protocol-specific negotiation
    9. Continue with request
"""

from hyproxy import Server, Asynclestener, Config


def main():
    """Create a basic listener."""
    
    print("""
[*] Basic Listener Example

The simplest possible listener setup.

Using all defaults except explicitly setting port.
    """)
    
    config = Config()
    
    # Create the simplest listener possible
    listener = Asynclestener(
        name='BasicListener',
        ip='0.0.0.0',
        port=1968,
        #protocols=[] Will use defaults
    )
    
    server = Server(listener)
    
    print("[*] Starting basic listener...")
    print("[*] Listening on: 0.0.0.0:1968")
    print("[*] Accessible from: Any machine (all interfaces)")
    print("[*] Protocols: HTTP, SOCKS4, SOCKS5 (auto-detected)")
    print()
    server.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
