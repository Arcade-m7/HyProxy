"""
DNS Utilities Example 1: DNS Caching System

HyProxy includes DNS resolver with automatic caching.

Key Features:

1. Async DNS Resolution
   - Non-blocking DNS queries
   - Multiple concurrent lookups
   - Timeout support

2. Automatic Caching
   - IPv4 and IPv6 separate caches
   - TTL: 3 minutes (180 seconds)
   - Reduces network traffic
   - Improves performance

3. Multiple Nameservers
   - Default: 8.8.8.8, 1.1.1.1
   - Public Google and Cloudflare DNS
   - Configurable: DNS.nameservers

4. Thread-Safe
   - Uses asyncio.Lock
   - Safe for concurrent use
   - No race conditions

5. Query Types
   - 'A': IPv4 address resolution
   - 'AAAA': IPv6 address resolution

DNS Cache Structure:

    DNSCACHE:
        ipv4: dict{domain -> CACHE(ip, expiry)}
        ipv6: dict{domain -> CACHE(ip, expiry)}

Where CACHE contains:
    - ip: Resolved IP address
    - timeex: Expiration timestamp

Usage Pattern:

    from hyproxy.utills.dns import DNS
    
    # Resolve IPv4
    ip = await DNS.resolve('example.com', 'A')
    
    # Resolve IPv6
    ip = await DNS.resolve('example.com', 'AAAA')
    
    # Set custom nameservers
    DNS.nameservers = ['1.1.1.1', '8.8.4.4']
    
    # Change TTL (cache lifetime)
    DNS.TTL = 300  # 5 minutes
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5


def main():
    """Explain DNS caching system."""
    
    print("""
[*] DNS Caching System:

Features:
    - Automatic IPv4 caching (type A records)
    - Automatic IPv6 caching (type AAAA records)
    - 3-minute TTL (Time To Live)
    - Thread-safe with locks
    - Multiple nameservers

Cache Benefits:
    - Fast repeated lookups
    - Reduced DNS traffic
    - Better performance
    - Lower latency

Example Scenario:

    First lookup of 'example.com':
        1. Query DNS server (e.g., 8.8.8.8)
        2. Get result (e.g., 93.184.216.34)
        3. Cache result for 3 minutes
        4. Return to client
    
    Second lookup (within 3 minutes):
        1. Check cache (HIT!)
        2. Return cached result
        3. No network query needed
        4. Much faster

    Third lookup (after 3 minutes):
        1. Check cache (EXPIRED)
        2. Query DNS server again
        3. Get new result
        4. Update cache
        5. Return to client

Nameservers (default):
    - 8.8.8.8 (Google DNS)
    - 1.1.1.1 (Cloudflare DNS)

You can customize:
    DNS.nameservers = ['1.1.1.1', '9.9.9.9']
    DNS.TTL = 600  # 10 minutes instead of 3
    """)
    
    config = Config()
    
    listener = Asynclestener(
        name='DNSCachingProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("\n[*] Starting server with DNS caching...")
    print()
    server.run()


if __name__ == '__main__':
    main()
