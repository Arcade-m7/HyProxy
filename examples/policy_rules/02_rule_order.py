"""
Policy Rules Example 2: Rule Evaluation and Order

Rules are evaluated in order. First match wins!

Critical: Order matters!

Example Scenario 1 - Wrong Order:

    Rule 1: DENY all ports
    Rule 2: ALLOW port 443
    
Result: Port 443 is also DENIED because Rule 1 matches first!

Example Scenario 2 - Correct Order:

    Rule 1: ALLOW port 443
    Rule 2: ALLOW port 80
    Rule 3: DENY all
    
Result: Ports 443 and 80 allowed, everything else denied.

Best Practices:

1. Specific rules first
   - More specific conditions first
   - General rules later

2. Whitelist strategy
   - ALLOW specific things
   - DENY everything (catch-all)

3. Blacklist strategy
   - DENY specific things
   - ALLOW everything (catch-all)

4. Default rule last
   - Always add a default rule at end
   - Catch anything that didn't match

Rule Evaluation Steps:

1. Connection arrives
2. First rule checked
   - If matches: Action applied (ALLOW or DENY)
   - If no match: Check next rule
3. Keep checking until match found
4. If no rule matches: Connection blocked (implicit DENY)
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS


def wrong_order_config():
    """Demonstrate wrong rule order."""
    config = Config()
    
    # WRONG: General rule first, specific rule never reached
    config.policy.addrule(
        SimpleRule(RouteInfo(), 'DENY all', ACTIONS.DENY)
    )
    
    # This rule never matches because DENY all matches first!
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=443)),
            'ALLOW HTTPS (unreachable!)',
            ACTIONS.ALLOW
        )
    )
    
    return config


def correct_order_config():
    """Demonstrate correct rule order."""
    config = Config()
    
    # CORRECT: Specific rules first
    
    # Rule 1: Allow HTTPS
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=443)),
            'ALLOW HTTPS',
            ACTIONS.ALLOW
        )
    )
    
    # Rule 2: Allow HTTP
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=80)),
            'ALLOW HTTP',
            ACTIONS.ALLOW
        )
    )
    
    # Rule 3: Allow DNS
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(port=53)),
            'ALLOW DNS',
            ACTIONS.ALLOW
        )
    )
    
    # Rule 4: Deny everything (catch-all at end)
    config.policy.addrule(
        SimpleRule(
            RouteInfo(),
            'DENY all (default)',
            ACTIONS.DENY
        )
    )
    
    return config


def main():
    """Create listeners with different rule orders."""
    
    print("""
[*] Rule Order is Critical!

Port 1968 (WRONG order):
    Rule 1: DENY all (matches everything!)
    Rule 2: ALLOW 443 (never reached)
    Result: Everything denied

Port 1969 (CORRECT order):
    Rule 1: ALLOW 443
    Rule 2: ALLOW 80
    Rule 3: ALLOW 53
    Rule 4: DENY all (catch-all)
    Result: Only 443, 80, 53 allowed
    """)
    
    wrong = wrong_order_config()
    wrong_listener = Asynclestener(
        name='WrongOrderProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(wrong), SOCKS5(wrong)]
    )
    
    correct = correct_order_config()
    correct_listener = Asynclestener(
        name='CorrectOrderProxy',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(correct), SOCKS5(correct)]
    )
    
    server = Server(wrong_listener, correct_listener)
    
    print("\n[*] Starting server with rule order examples...")
    print()
    server.run()


if __name__ == '__main__':
    main()
