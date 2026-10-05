"""
Policy Rules Example 3: Complex Rule Combinations

Build sophisticated policies by combining multiple rules.

Pattern 1: Department Access Control

Different departments access different resources.

    Marketing dept (10.0.1.0/24):
    - Web only (ports 80, 443)
    - Social media APIs
    
    Engineering dept (10.0.2.0/24):
    - Web + SSH + Git
    - Internal servers
    
    Executive (10.0.3.0/24):
    - Full access

Pattern 2: Time-based Security (concept)

Different rules could be applied at different times:
    - Office hours: Restricted
    - After hours: Blocked
    - Weekends: Blocked

Pattern 3: Geographic Restrictions

Allow only certain destinations:
    - US IPs: Allowed
    - EU IPs: Allowed
    - Others: Blocked

Pattern 4: Progressive Restrictions

Higher security for higher risk:
    - Guest users: HTTP/HTTPS only
    - Staff: + SSH, + VPN
    - Admins: Full access
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS5
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS


def department_access_policy():
    """Create policy with department-based access control."""
    config = Config()
    
    # Marketing: Web only
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.0.1.0/24'),
                dst=NETADDRESS(port=[80, 443])
            ),
            'Marketing - Web access',
            ACTIONS.ALLOW
        )
    )
    
    # Engineering: Web + SSH + DNS
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.0.2.0/24'),
                dst=NETADDRESS(port=[80, 443, 22, 53])
            ),
            'Engineering - Extended access',
            ACTIONS.ALLOW
        )
    )
    
    # Engineering: Also allow internal servers
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.0.2.0/24'),
                dst=NETADDRESS(ip='192.168.0.0/16')
            ),
            'Engineering - Internal access',
            ACTIONS.ALLOW
        )
    )
    
    # Executive: Allow from 10.0.3.0/24
    config.policy.addrule(
        SimpleRule(
            RouteInfo(src=NETADDRESS(ip='10.0.3.0/24')),
            'Executive - Full access',
            ACTIONS.ALLOW
        )
    )
    
    # Block internal networks from any external source
    config.policy.addrule(
        SimpleRule(
            RouteInfo(dst=NETADDRESS(ip='192.168.0.0/16')),
            'Block external to internal',
            ACTIONS.DENY
        )
    )
    
    # Deny everything else
    config.policy.addrule(
        SimpleRule(
            RouteInfo(),
            'Default deny',
            ACTIONS.DENY
        )
    )
    
    return config


def security_tiers_policy():
    """Create policy with security tiers."""
    config = Config()
    
    # Guest: HTTPS only
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.1.0.0/24'),
                dst=NETADDRESS(port=443)
            ),
            'Guest tier - HTTPS only',
            ACTIONS.ALLOW
        )
    )
    
    # Staff: Web + DNS
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.2.0.0/24'),
                dst=NETADDRESS(port=[80, 443, 53])
            ),
            'Staff tier - Web + DNS',
            ACTIONS.ALLOW
        )
    )
    
    # Admin: Internal access
    config.policy.addrule(
        SimpleRule(
            RouteInfo(
                src=NETADDRESS(ip='10.3.0.0/24'),
                dst=NETADDRESS(ip='192.168.0.0/16')
            ),
            'Admin tier - Internal access',
            ACTIONS.ALLOW
        )
    )
    
    # Deny everything else
    config.policy.addrule(
        SimpleRule(
            RouteInfo(),
            'Default deny',
            ACTIONS.DENY
        )
    )
    
    return config


def main():
    """Create listeners with complex policies."""
    
    dept_config = department_access_policy()
    dept_listener = Asynclestener(
        name='DepartmentAccessProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(dept_config), SOCKS5(dept_config)]
    )
    
    tiers_config = security_tiers_policy()
    tiers_listener = Asynclestener(
        name='SecurityTiersProxy',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(tiers_config), SOCKS5(tiers_config)]
    )
    
    server = Server(dept_listener, tiers_listener)
    
    print("""
[*] Complex Policy Examples:

Port 1968 (Department Access):
    Marketing (10.0.1.0/24): Web only (80, 443)
    Engineering (10.0.2.0/24): Web + SSH + DNS + Internal
    Executive (10.0.3.0/24): Full access
    Others: Denied

Port 1969 (Security Tiers):
    Guest (10.1.0.0/24): HTTPS only
    Staff (10.2.0.0/24): Web + DNS
    Admin (10.3.0.0/24): Internal network access
    Others: Denied
    """)
    
    print("\n[*] Starting server with complex policies...")
    print()
    server.run()


if __name__ == '__main__':
    main()
