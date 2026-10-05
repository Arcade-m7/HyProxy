"""
Policy Rules Example 1: SimpleRule Basics

SimpleRule combines:
1. RouteInfo - What to match
2. Action - What to do (ALLOW or DENY)
3. Name - Human-readable description

Structure:

SimpleRule(
    tunnel=RouteInfo(...),  # What to match
    name='Rule name',       # Description
    action=ACTIONS.ALLOW    # What to do
)

Rule Matching:

A SimpleRule matches a tunnel if:
- The RouteInfo matches the tunnel

When matched:
- If action=ALLOW: Connection proceeds
- If action=DENY: Connection is blocked

Properties:

- rule.tunnel: RouteInfo object
- rule.action: ALLOW (1) or DENY (0)
- rule.name: Description string
- rule(tunnel): Call to check if matches

Evaluation:

Rules are checked in order added:
1. First rule that matches wins
2. Others are ignored
3. Order is critical!
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS


def simple_rule_example():
    """Create config with simple rules."""
    config = Config()
    
    print("""
[*] SimpleRule Examples:

Rule 1: Allow HTTPS
    SimpleRule(
        tunnel=RouteInfo(dst=NETADDRESS(port=443)),
        name='Allow HTTPS',
        action=ACTIONS.ALLOW
    )

Rule 2: Block internal network
    SimpleRule(
        tunnel=RouteInfo(dst=NETADDRESS(ip='192.168.0.0/16')),
        name='Block internal',
        action=ACTIONS.DENY
    )

Rule 3: Allow from admin
    SimpleRule(
        tunnel=RouteInfo(src=NETADDRESS(ip='10.0.0.5')),
        name='Allow admin',
        action=ACTIONS.ALLOW
    )
    """)
    
    # Add simple rules
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=443)),
            'Allow HTTPS',
            ACTIONS.ALLOW
        )
    )
    
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=80)),
            'Allow HTTP',
            ACTIONS.ALLOW
        )
    )
    
    config.policy.addrule(
        SimpleRule(
            RouteInfo(),
            'Deny everything else',
            ACTIONS.DENY
        )
    )
    
    return config


def main():
    """Create a server with simple rules."""
    
    config = simple_rule_example()
    
    listener = Asynclestener(
        name='SimpleRuleProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(config), SOCKS5(config)]
    )
    
    server = Server(listener)
    
    print("\n[*] Starting server with SimpleRule policy...")
    print()
    server.run()


if __name__ == '__main__':
    main()
