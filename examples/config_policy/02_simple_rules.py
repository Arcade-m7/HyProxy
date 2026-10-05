"""
Config Policy Example 2: Simple Allow/Deny Rules

This example uses the real policy API:

    config.policy.addrule(SimpleRule(RouteInfo(...), name, ACTIONS.ALLOW))
    config.policy.addrule(SimpleRule(RouteInfo(...), name, ACTIONS.DENY))

Rules are evaluated from first to last. The first matching rule returns
bool(rule.action). If no rule matches, Policy returns True and allows traffic.

This file also shows domain blocking with NETADDRESS(domain='www.example.com').
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS


def build_config() -> Config:
    """Block one domain, allow common web/DNS ports, and deny everything else."""
    config = Config()

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(domain='www.example.com')),
        'Block www.example.com',
        ACTIONS.DENY,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(port=443)),
        'Allow HTTPS',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(port=80)),
        'Allow HTTP',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(dst=NETADDRESS(port=53)),
        'Allow DNS',
        ACTIONS.ALLOW,
    ))

    config.policy.addrule(SimpleRule(
        RouteInfo(),
        'Deny everything else',
        ACTIONS.DENY,
    ))

    return config


def explain_policy(config: Config) -> None:
    """Print rule order and sample decisions."""
    print("[*] Rules, in evaluation order:")
    for index, rule in enumerate(config.policy.showrules(), start=1):
        print(f"    {index}. {rule.name}: action={rule.action}, match={rule.tunnel}")

    samples = [
        ('blocked domain', RouteInfo(dst=NETADDRESS(domain='www.example.com', port=443))),
        ('HTTPS', RouteInfo(dst=NETADDRESS(domain='www.python.org', port=443))),
        ('HTTP', RouteInfo(dst=NETADDRESS(domain='www.python.org', port=80))),
        ('DNS', RouteInfo(dst=NETADDRESS(port=53))),
        ('SSH', RouteInfo(dst=NETADDRESS(port=22))),
    ]

    print("[*] Sample decisions:")
    for label, route in samples:
        print(f"    {label:14} -> {config.policy(route)}")


def main():
    """Start a proxy that blocks one domain and allows selected ports."""
    config = build_config()

    print("[*] Simple Policy Rules example")
    print("[*] True means allowed; False means denied.")
    explain_policy(config)
    print()

    listener = Asynclestener(
        name='RestrictedProxy',
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