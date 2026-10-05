# Policy Rules Examples

Rule engine for creating routing policies.

## What is SimpleRule?

SimpleRule combines:
- RouteInfo (what to match)
- Action (ALLOW or DENY)
- Name (description)

Rules are evaluated in order - first match wins!

## API Overview

```python
SimpleRule(
    tunnel=RouteInfo(...),
    name='Rule description',
    action=ACTIONS.ALLOW
)
```

## Files

### 01_simple_rules.py
Basic rule creation and usage.

```bash
python 01_simple_rules.py
```

Examples:
- Simple port allow
- Default deny catch-all
- Basic rule structure

### 02_rule_order.py
Understanding rule evaluation order.

```bash
python 02_rule_order.py
```

Critical concepts:
- Order matters!
- First match wins
- Specific rules first
- Default rule last

### 03_complex_combinations.py
Real-world policy scenarios.

```bash
python 03_complex_combinations.py
```

Examples:
- Department access control
- Security tier policies
- Multi-network rules

## Rule Creation Pattern

```python
config = Config()

# Specific rules first
config.policy.addrule(SimpleRule(
    RouteInfo(dst=NETADDRESS(port=443)),
    'Allow HTTPS',
    ACTIONS.ALLOW
))

config.policy.addrule(SimpleRule(
    RouteInfo(dst=NETADDRESS(port=80)),
    'Allow HTTP',
    ACTIONS.ALLOW
))

# Default rule last
config.policy.addrule(SimpleRule(
    RouteInfo(),
    'Deny all',
    ACTIONS.DENY
))
```

## Best Practices

### Rule Order

```
Correct:
  1. Allow port 443
  2. Allow port 80
  3. Deny all

Wrong:
  1. Deny all        <- Matches everything!
  2. Allow port 443  <- Never reached
```

### Whitelist Strategy

```python
# Allow specific things
addrule(ALLOW HTTP)
addrule(ALLOW HTTPS)
addrule(ALLOW DNS)

# Deny everything else (catch-all)
addrule(DENY all)
```

### Blacklist Strategy

```python
# Block specific things
addrule(DENY internal)
addrule(DENY reserved_ports)

# Allow everything else (catch-all)
addrule(ALLOW all)
```

## Real-World Examples

### Department Access

```python
# Marketing: Web only
addrule(SimpleRule(
    RouteInfo(
        src=NETADDRESS(ip='10.0.1.0/24'),
        dst=NETADDRESS(port=[80, 443])
    ),
    'Marketing web access',
    ACTIONS.ALLOW
))

# Engineering: Web + SSH + Internal
addrule(SimpleRule(
    RouteInfo(
        src=NETADDRESS(ip='10.0.2.0/24'),
        dst=NETADDRESS(port=[80, 443, 22, 53])
    ),
    'Engineering access',
    ACTIONS.ALLOW
))
```

## Learning Path

1. Start with **01_simple_rules.py**
2. Study **02_rule_order.py** (CRITICAL!)
3. Analyze **03_complex_combinations.py**

## Important Notes

- **Order is critical**: First match wins
- **Always add default**: Catch-all rule at end
- **Test your rules**: Verify access patterns
- **Specific first**: More specific conditions first
- **Monitor traffic**: Log to track denials

## Reference

For implementation details, see `hyproxy/policy/rules.py`
