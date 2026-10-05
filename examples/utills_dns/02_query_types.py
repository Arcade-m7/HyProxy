"""
DNS Utilities Example 2: Query Types and Resolution

DNS supports two query types: A (IPv4) and AAAA (IPv6).

Query Type: 'A'
    - IPv4 address records
    - Returns: IPv4 address (e.g., 93.184.216.34)
    - Type: 32-bit address
    - Example: A record for example.com -> 93.184.216.34

Query Type: 'AAAA'
    - IPv6 address records
    - Returns: IPv6 address (e.g., 2606:2800:220:1:248:1893:25c8:1946)
    - Type: 128-bit address
    - Example: AAAA record for example.com -> 2606:2800:220:1:248:1893:25c8:1946

Resolution Flow:

    DNS.resolve(domain='example.com', qtype='A')
    
    1. Check if domain is valid
    2. Check IPv4 cache
    3. If cached: Return result
    4. If not cached:
       a. Create DNSResolver
       b. Send query to nameserver
       c. Parse response
       d. Store in cache
       e. Return result

Result Handling:

    Success:
        Returns: '93.184.216.34' (string)
    
    Cache Hit:
        Returns: Cached result (no network query)
    
    Failure:
        Returns: None

Error Conditions:

    - Domain doesn't exist: None
    - DNS server unreachable: None
    - Timeout: None
    - Invalid query type: Assertion error
    - No IPv6 support: None (for AAAA queries)

Performance Comparison:

    First query (cache miss):
        Time: ~50-200ms (depends on network)
    
    Subsequent queries (cache hit):
        Time: <1ms (just lookup in dict)
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5


def dns_resolution_info():
    """Print DNS resolution information."""
    print("""
[*] DNS Resolution Types:

IPv4 Resolution ('A' queries):

    DNS.resolve('example.com', 'A')
    Returns: '93.184.216.34'
    
    Use when: IPv4 addresses needed
    Performance: Fast (cached after first query)

IPv6 Resolution ('AAAA' queries):

    DNS.resolve('example.com', 'AAAA')
    Returns: '2606:2800:220:1:248:1893:25c8:1946'
    
    Use when: IPv6 addresses needed
    Performance: Fast (cached after first query)

Example Addresses:

    IPv4 (type A):
        - 8.8.8.8 (Google DNS)
        - 1.1.1.1 (Cloudflare DNS)
        - 93.184.216.34 (example.com)
    
    IPv6 (type AAAA):
        - 2001:4860:4860::8888 (Google DNS)
        - 2606:4700:4700::1111 (Cloudflare DNS)
        - 2606:2800:220:1:248:1893:25c8:1946 (example.com)

Cache Strategy:

    Each query cached separately:
    - 'example.com' + 'A' -> cached
    - 'example.com' + 'AAAA' -> cached separately
    
    Expiration after 3 minutes (configurable)
    Fresh queries trigger new DNS lookups
    """)


def main():
    """Explain DNS query types and resolution."""
    
    dns_resolution_info()
    
    config = Config()
    
    # Optionally enable IPv6 for AAAA queries
    try:
        config.connection.ipv6.enable()
    except:
        pass
    
    listener = Asynclestener(
        name='DNSResolutionProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("\n[*] Starting server with DNS resolution...")
    print()
    server.run()


if __name__ == '__main__':
    main()
