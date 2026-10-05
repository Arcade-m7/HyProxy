"""
Config Policy Example 3: Advanced Routing

This example combines source networks, destination networks, destination ports,
destination domains, and a final catch-all rule. It is based on the current
hyproxy.policy models:

- NETADDRESS(ip=...) accepts IP strings and CIDR networks.
- NETADDRESS(port=...) accepts int, range, or list.
- NETADDRESS(domain=...) matches a destination domain such as www.example.com.
- RouteInfo(src=..., dst=...) combines optional source and destination matches.
- SimpleRule(..., ACTIONS.ALLOW/DENY) decides the result of the first match.

Note: when a rule contains src=NETADDRESS(...), the route being evaluated should
also include src=NETADDRESS(...). Runtime proxy routes include a source address;
these demo routes do the same so matching behaves like live traffic.
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS


def build_config() -> Config:
    """Create a policy with ordered domain, source, and destination rules."""
    config = Config()

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(domain='www.example.com')),
        'Block www.example.com',
        ACTIONS.DENY,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(
            src=NETADDRESS(ip='192.168.1.0/24'),
            dst=NETADDRESS(ip='192.168.2.0/24'),
        ),
        'Allow internal network traffic',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(port=53)),
        'Allow DNS',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(ip='192.168.0.0/16', port=range(1, 1025))),
        'Block reserved ports to internal network',
        ACTIONS.DENY,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(port=[80, 443])),
        'Allow web browsing',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(),
        'Default deny',
        ACTIONS.DENY,
    ))

    return config


def demo_route(src_ip: str, dst_ip: str, dst_port: int, dst_domain: str | None = None) -> RouteInfo:
    """Build a complete source/destination route like the proxy runtime does."""
    return RouteInfo(
        src=NETADDRESS(ip=src_ip),
        dst=NETADDRESS(ip=dst_ip, port=dst_port, domain=dst_domain),
    )


def explain_policy(config: Config) -> None:
    """Print rule order and sample routing decisions."""
    print("[*] Rules, in evaluation order:")
    for index, rule in enumerate(config.policy.showrules(), start=1):
        print(f"    {index}. {rule.name}: action={rule.action}, match={rule.tunnel}")

    samples = [
        ('blocked domain', demo_route('10.0.0.25', '93.184.216.34', 443, 'www.example.com')),
        ('internal to internal', demo_route('192.168.1.50', '192.168.2.25', 8080)),
        ('dns', demo_route('10.0.0.25', '8.8.8.8', 53)),
        ('internal ssh blocked', demo_route('10.0.0.25', '192.168.10.10', 22)),
        ('public https allowed', demo_route('10.0.0.25', '93.184.216.34', 443, 'www.python.org')),
        ('public ssh denied', demo_route('10.0.0.25', '93.184.216.34', 22)),
    ]

    print("[*] Sample decisions:")
    for label, route in samples:
        print(f"    {label:22} -> {config.policy(route)}")


def main():
    """Start a proxy with advanced source/destination policy rules."""
    config = build_config()

    print("[*] Advanced Policy example")
    print("[*] True means allowed; False means denied.")
    explain_policy(config)
    print()

    listener = Asynclestener(
        name='AdvancedPolicyProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)],
    )

    print("[*] Starting proxy on 127.0.0.1:1968")
    print("[*] Press Ctrl+C to stop")
    Server(listener).run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Server stopped")