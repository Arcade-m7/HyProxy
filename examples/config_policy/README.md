# Config Policy Examples

These examples are synchronized with the current `hyproxy/policy` implementation. A policy is a list of `SimpleRule` objects evaluated from first to last.

## Real API

```python
from hyproxy import Config
from hyproxy.policy import SimpleRule, RouteInfo, ACTIONS, NETADDRESS

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

allowed = config.policy(RouteInfo(dst=NETADDRESS(domain='www.python.org', port=443)))
blocked = config.policy(RouteInfo(dst=NETADDRESS(domain='www.example.com', port=443)))
```

## Behavior From `hyproxy/policy`

- `Policy.__call__(info)` returns `bool(rule.action)` for the first matching rule.
- `ACTIONS.ALLOW` is `1`, so matching allow rules return `True`.
- `ACTIONS.DENY` is `0`, so matching deny rules return `False`.
- If no rules match, `Policy.__call__` returns `True` and allows traffic.
- `RouteInfo()` with no `src` or `dst` matches everything, so use it only as a final catch-all.
- If a rule includes `src=NETADDRESS(...)`, evaluate it with routes that also include `src`; live proxy routes include source addresses.

## Files

- `01_no_policy.py` - demonstrates the default allow-all behavior of an empty policy.
- `02_simple_rules.py` - blocks `www.example.com`, allows HTTPS, HTTP, and DNS, then denies everything else.
- `03_advanced_routing.py` - combines domain blocking, source CIDR, destination CIDR, port lists, port ranges, and a default deny rule.

Run one from the project root:

```powershell
python examples/config_policy/02_simple_rules.py
```

Each script prints sample policy decisions before starting the proxy server.

## Matching Models

```python
NETADDRESS(ip='192.168.1.0/24')        # IP or CIDR network
NETADDRESS(ip='192.168.1.10')          # Single IP
NETADDRESS(port=443)                   # Single port
NETADDRESS(port=[80, 443])             # Port list
NETADDRESS(port=range(1, 1025))        # Port range
NETADDRESS(domain='www.example.com')   # Domain name

RouteInfo(src=NETADDRESS(ip='10.0.0.0/8'))
RouteInfo(dst=NETADDRESS(port=443))
RouteInfo(dst=NETADDRESS(domain='www.example.com'))
RouteInfo(src=NETADDRESS(ip='10.0.0.0/8'), dst=NETADDRESS(port=443))
```

## Domain Blocking

Put domain deny rules before broader allow rules:

```python
config.policy.addrule(SimpleRule(
    RouteInfo(dst=NETADDRESS(domain='www.example.com')),
    'Block www.example.com',
    ACTIONS.DENY,
))

config.policy.addrule(SimpleRule(
    RouteInfo(dst=NETADDRESS(port=[80, 443])),
    'Allow web browsing',
    ACTIONS.ALLOW,
))
```

A request route like this will be denied:

```python
RouteInfo(dst=NETADDRESS(domain='www.example.com', port=443))
```

## Rule Order

Use specific rules first and broad rules last:

```python
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
    RouteInfo(),
    'Deny everything else',
    ACTIONS.DENY,
))
```

Putting `RouteInfo()` first will match every route and prevent later rules from being used. That is the policy equivalent of putting a sofa in front of every door.