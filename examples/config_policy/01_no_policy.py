"""
Config Policy Example 1: No Policy (Allow All)

This example mirrors the real behavior in hyproxy/policy/policy.py:

    Policy.__call__(route_info)

returns True when no rule matches. A fresh Config creates an empty Policy, so
all routes are allowed until you add SimpleRule objects with config.policy.addrule().
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.policy import RouteInfo, NETADDRESS


def explain_policy(config: Config) -> None:
    """Show what an empty policy does before the server starts."""
    sample_route = RouteInfo(dst=NETADDRESS(port=443))

    print("[*] Policy rules:", config.policy.showrules())
    print("[*] Sample route:", sample_route)
    print("[*] Policy result:", config.policy(sample_route), "(True means allowed)")


def main():
    """Create a proxy with no policy restrictions."""
    config = Config()

    print("[*] No Policy example")
    print("[*] A new Config has an empty Policy, so unmatched traffic is allowed.")
    explain_policy(config)
    print()

    listener = Asynclestener(
        name='AllowAllProxy',
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