"""
DNS Utilities Example 3: Advanced DNS Configuration

Customize DNS settings for your needs.

Customization Options:

1. Change Nameservers
   
   Default: ['8.8.8.8', '1.1.1.1']
   
   Set custom:
       DNS.nameservers = ['1.1.1.1', '9.9.9.9']
       DNS.nameservers = ['208.67.222.222']  # OpenDNS
       DNS.nameservers = ['8.26.56.26']  # Comodo DNS

2. Adjust TTL (Time To Live)
   
   Default: 60 * 3 = 180 seconds (3 minutes)
   
   Shorter TTL (faster updates):
       DNS.TTL = 60  # 1 minute
   
   Longer TTL (better performance):
       DNS.TTL = 600  # 10 minutes
       DNS.TTL = 3600  # 1 hour

Use Cases:

1. Private DNS Network
   
   DNS.nameservers = ['192.168.1.1']  # Internal DNS
   DNS.TTL = 300  # 5 minutes
   
   Good for: Corporate networks

2. Privacy-Focused
   
   DNS.nameservers = ['1.1.1.1', '9.9.9.9']
   DNS.TTL = 180  # Standard
   
   Good for: Privacy concerns

3. Maximum Performance
   
   DNS.TTL = 3600  # Cache for 1 hour
   
   Good for: High-traffic proxies

4. Always Fresh
   
   DNS.TTL = 60  # Cache for 1 minute
   
   Good for: Dynamic environments

Cache Management:

    # View current cache size
    ipv4_cached = len(DNS.cache.ipv4)
    ipv6_cached = len(DNS.cache.ipv6)
    
    # Access cache directly (if needed)
    # DNS.cache.ipv4['example.com'] = CACHE(ip, expiry)

DNS Fallback:

    BaseProtocol.dnsrb() provides fallback:
    1. Try enabled IP version (IPv6 if enabled)
    2. Fall back to other version if failed
    3. Return first successful result
    4. Return None if all fail
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5
from hyproxy.utills.dns import DNS


def internal_network_config():
    """Config for internal network with private DNS."""
    
    # Configure internal DNS
    DNS.nameservers = ['192.168.1.1', '192.168.1.2']
    DNS.TTL = 300  # 5 minutes cache
    
    config = Config()
    return config


def privacy_focused_config():
    """Config for privacy-focused proxy."""
    
    # Use privacy-respecting DNS
    DNS.nameservers = ['1.1.1.1', '9.9.9.9']
    DNS.TTL = 180  # 3 minutes cache
    
    config = Config()
    return config


def performance_focused_config():
    """Config for maximum performance."""
    
    # Longer cache TTL for better performance
    DNS.nameservers = ['8.8.8.8', '8.8.4.4']
    DNS.TTL = 3600  # 1 hour cache
    
    config = Config()
    return config


def main():
    """Create proxies with different DNS configurations."""
    
    print("""
[*] Advanced DNS Configuration Examples:

Port 1968 (Internal Network):
    Nameservers: 192.168.1.1, 192.168.1.2
    TTL: 5 minutes
    Purpose: Corporate internal DNS
    
Port 1969 (Privacy Focused):
    Nameservers: 1.1.1.1 (Cloudflare), 9.9.9.9 (Quad9)
    TTL: 3 minutes
    Purpose: Privacy-respecting DNS
    
Port 1970 (Performance Optimized):
    Nameservers: 8.8.8.8, 8.8.4.4 (Google)
    TTL: 1 hour
    Purpose: High-traffic, caching-focused

Benefits of Customization:

    Internal DNS:
        - Faster resolution of internal domains
        - Better security (no external queries)
        - Reduced external traffic

    Privacy DNS:
        - Non-logging servers
        - Better privacy
        - Still fast performance

    Performance DNS:
        - Longer cache lifetime
        - Fewer network queries
        - Better throughput
        - Less latency variation
    """)
    
    # Reset to defaults first
    DNS.nameservers = ['8.8.8.8', '1.1.1.1']
    DNS.TTL = 180
    
    internal = internal_network_config()
    internal_listener = Asynclestener(
        name='InternalDNSProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(internal), SOCKS5(internal)]
    )
    
    privacy = privacy_focused_config()
    privacy_listener = Asynclestener(
        name='PrivacyDNSProxy',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(privacy), SOCKS5(privacy)]
    )
    
    performance = performance_focused_config()
    perf_listener = Asynclestener(
        name='PerformanceDNSProxy',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(performance), SOCKS5(performance)]
    )
    
    server = Server(internal_listener, privacy_listener, perf_listener)
    
    print("\n[*] Starting server with advanced DNS configurations...")
    print()
    server.run()


if __name__ == '__main__':
    main()
