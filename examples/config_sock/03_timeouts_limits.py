"""
Config Socket Example 3: Timeout and Connection Limits

Control operation timeouts and concurrent connection limits.

Timeout:
- Default: 60 seconds
- Applies to socket operations (send, receive)
- Prevents hanging connections
- Lower = faster detection of dead connections
- Higher = more tolerance for slow networks

Max Connections:
- Default: None (unlimited)
- Limits concurrent connections
- Useful for resource management
- Prevents resource exhaustion
- Uses asyncio.Semaphore internally

Use Cases:

1. Fast networks with high reliability:
   - Lower timeout (e.g., 30 seconds)
   - Higher max connections

2. Slow or unreliable networks:
   - Higher timeout (e.g., 120 seconds)
   - Lower max connections

3. Mobile/cellular:
   - Higher timeout (e.g., 180 seconds)
   - Lower max connections for stability

4. Production server:
   - Moderate timeout (60-90 seconds)
   - Limited connections (e.g., 1000-5000)
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5


def create_fast_config():
    """Config for fast, reliable networks."""
    config = Config()
    config.connection.timeout = 30  # 30 seconds
    config.connection.setmaxconnections(5000)  # 5000 concurrent
    return config


def create_stable_config():
    """Config for standard operations."""
    config = Config()
    config.connection.timeout = 60  # 60 seconds (default)
    config.connection.setmaxconnections(1000)  # 1000 concurrent
    return config


def create_resilient_config():
    """Config for slow/unreliable networks."""
    config = Config()
    config.connection.timeout = 120  # 120 seconds
    config.connection.setmaxconnections(500)  # 500 concurrent
    return config


def main():
    """Create listeners with different timeout/connection settings."""
    
    fast = create_fast_config()
    fast_listener = Asynclestener(
        name='FastNetwork',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(fast), SOCKS5(fast)]
    )
    
    stable = create_stable_config()
    stable_listener = Asynclestener(
        name='StableNetwork',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(stable), SOCKS5(stable)]
    )
    
    resilient = create_resilient_config()
    resilient_listener = Asynclestener(
        name='ResilientNetwork',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(resilient), SOCKS5(resilient)]
    )
    
    server = Server(fast_listener, stable_listener, resilient_listener)
    
    print("[*] Starting server with different socket configurations...")
    print()
    print("[*] Port 1968 (Fast Network):")
    print(f"    Timeout: {fast_listener.protocols[0].config.connection.timeout}s")
    print(f"    Max connections: {fast_listener.protocols[0].config.connection.max_connections}")
    print()
    print("[*] Port 1969 (Stable Network):")
    print(f"    Timeout: {stable_listener.protocols[0].config.connection.timeout}s")
    print(f"    Max connections: {stable_listener.protocols[0].config.connection.max_connections}")
    print()
    print("[*] Port 1970 (Resilient Network):")
    print(f"    Timeout: {resilient_listener.protocols[0].config.connection.timeout}s")
    print(f"    Max connections: {resilient_listener.protocols[0].config.connection.max_connections}")
    print()
    server.run()


if __name__ == '__main__':
    main()
