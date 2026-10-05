# HyProxy Examples Documentation

This folder contains comprehensive examples demonstrating all HyProxy components, from simple to advanced.

## Folder Structure

### 1. `server/` - Server Management
Examples showing how the Server class works:
- **01_basic_server.py** - Create a server with one listener (simplest setup)
- **02_multiple_listeners.py** - Run multiple listeners simultaneously
- **03_different_ips.py** - Listeners on different network interfaces

**Key Concepts:**
- Server manages Asynclestener objects
- Server starts the asyncio event loop
- Multiple listeners run concurrently in one server

---

### 2. `asynclestener/` - Listeners
Examples showing how Asynclestener works:
- **01_basic_listener.py** - Listener with default settings
- **02_named_listeners.py** - Named listeners with specific protocol support

**Key Concepts:**
- Asynclestener listens on IP:port
- Auto-detects client protocol
- Routes connections to appropriate handler
- Each listener can support different protocols

---

### 3. `config_auth/` - Authentication
Examples showing authentication in Config:
- **01_no_auth.py** - Server without authentication (allow all)
- **02_basic_auth.py** - Single username/password
- **03_multiple_credentials.py** - Different credentials per listener

**Key Concepts:**
- Credentials stored as bytes: `b'username'`
- Different listeners can have different credentials
- No auth means: anyone can connect
- With auth means: client must provide credentials

---

### 4. `config_cmd/` - Command Support
Examples showing command functionality in Config:
- **01_basic_cmd.py** - Enable command support
- **02_cmd_toggle.py** - Enable/disable commands on different listeners

**Key Concepts:**
- Commands let clients control proxy behavior
- Enable/disable operations
- Check status with `get()`
- Can be different per listener

---

### 5. `config_log/` - Logging
Examples showing logging in Config:
- **01_basic_logging.py** - Enable logging for monitoring
- **02_logging_control.py** - Different logging levels per listener

**Key Concepts:**
- Logging records all proxy activity
- Useful for debugging and auditing
- Can enable/disable per listener
- Performance vs. monitoring tradeoff

---

### 6. `config_policy/` - Policy and Routing
Examples showing policy rules in Config:
- **01_no_policy.py** - No restrictions (allow everything)
- **02_simple_rules.py** - Simple allow/deny by port
- **03_advanced_routing.py** - Complex rules with CIDR notation

**Key Concepts:**
- Routes: Source and destination matching
- Actions: ALLOW or DENY
- Rules evaluated in order (first match wins)
- CIDR notation: 192.168.1.0/24
- Ports: Single value or range()

---

### 7. `protocols/` - Protocol Support
Examples showing different protocols:
- **01_http_protocol.py** - HTTP only (web browsing)
- **02_socks4_protocol.py** - SOCKS4 only (legacy)
- **03_socks5_protocol.py** - SOCKS5 only (modern)
- **04_mixed_protocols.py** - All three protocols with auto-detection

**Key Concepts:**
- HTTP: Web traffic (port 80)
- SOCKS4: Legacy proxy protocol
- SOCKS5: Modern proxy protocol with auth
- Auto-detection: First byte determines protocol

---

### 8. `config_sock/` - Socket Configuration
Examples showing socket-level network configuration:
- **01_connection_overview.py** - Default connection settings
- **02_ip_versions.py** - IPv4 and IPv6 support
- **03_timeouts_limits.py** - Timeouts and connection limits

**Key Concepts:**
- IPv4/IPv6 support control
- Connection timeouts
- Max concurrent connections
- DNS resolution settings

---

### 9. `net_network/` - Network Utilities
Examples showing network I/O and protocol detection:
- **01_protocol_detection.py** - Automatic protocol detection
- **02_stream_operations.py** - Stream I/O operations

**Key Concepts:**
- BytesParser: Detect protocol from first byte
- Stream: Async I/O with counting and timeouts
- Multiple protocols on one port
- Data transfer tracking

---

### 10. `policy_models/` - Policy Data Models
Examples showing policy models and routing criteria:
- **01_netaddress_ports_ips.py** - NETADDRESS, PORT, IP models
- **02_routeinfo.py** - Source and destination matching
- **03_actions.py** - ALLOW vs DENY strategies

**Key Concepts:**
- IP addresses and CIDR ranges
- Port specifications and ranges
- Source/destination matching
- Whitelist vs blacklist strategies

---

### 11. `policy_rules/` - Policy Rule Engine
Examples showing how to create and combine rules:
- **01_simple_rules.py** - Basic rule creation
- **02_rule_order.py** - Rule evaluation order (CRITICAL!)
- **03_complex_combinations.py** - Real-world scenarios

**Key Concepts:**
- SimpleRule structure
- Rule order matters (first match wins)
- Department/tier-based access
- Complex multi-rule policies

---

### 12. `protocols_base/` - Base Protocol Class
Examples showing protocol inheritance and features:
- **01_baseprotocol_overview.py** - BaseProtocol features
- **02_dns_resolution.py** - DNS resolution methods
- **03_complete_config.py** - Enterprise configuration

**Key Concepts:**
- Protocol inheritance
- Configuration integration
- DNS resolution (IPv4/IPv6)
- Connection management

---

### 13. `utills_dns/` - DNS Utilities
Examples showing DNS caching and resolution:
- **01_dns_caching.py** - Automatic DNS caching
- **02_query_types.py** - IPv4 and IPv6 queries
- **03_advanced_config.py** - Custom DNS configurations

**Key Concepts:**
- DNS caching (3-minute TTL)
- Type A (IPv4) and AAAA (IPv6)
- Custom nameservers
- Privacy and performance options

---

## Quick Start Examples

### Start with simplest setup:
```bash
python server/01_basic_server.py
```

### Learn listeners:
```bash
python asynclestener/02_named_listeners.py
```

### Add authentication:
```bash
python config_auth/02_basic_auth.py
```

### Add policies:
```bash
python config_policy/02_simple_rules.py
```

### Understand policy rules (CRITICAL!):
```bash
python policy_rules/02_rule_order.py
```

### Use different protocols:
```bash
python protocols/04_mixed_protocols.py
```

### Network configuration:
```bash
python config_sock/02_ip_versions.py
```

### DNS and caching:
```bash
python utills_dns/01_dns_caching.py
```

---

## Learning Path (Recommended Order)

### Foundation (Understanding HyProxy)
1. `server/01_basic_server.py` - Server basics
2. `asynclestener/01_basic_listener.py` - Listener basics
3. `protocols/04_mixed_protocols.py` - Protocol support

### Configuration Basics
4. `config_auth/02_basic_auth.py` - Authentication
5. `config_sock/01_connection_overview.py` - Connection settings

### Policies (Important!)
6. `policy_models/01_netaddress_ports_ips.py` - Understanding models
7. `policy_rules/01_simple_rules.py` - Basic rules
8. **`policy_rules/02_rule_order.py` - CRITICAL: Order matters!**
9. `config_policy/02_simple_rules.py` - Simple routing policies

### Advanced Features
10. `config_cmd/02_cmd_toggle.py` - Command control
11. `config_log/02_logging_control.py` - Logging options
12. `protocols_base/02_dns_resolution.py` - DNS resolution
13. `utills_dns/02_query_types.py` - DNS query types

### Real-World Scenarios
14. `policy_models/03_actions.py` - Allow/Deny strategies
15. `policy_rules/03_complex_combinations.py` - Complex policies
16. `protocols_base/03_complete_config.py` - Enterprise setup
17. `utills_dns/03_advanced_config.py` - Advanced DNS
18. `net_network/02_stream_operations.py` - Stream I/O

---

## Key Concepts Summary

### Server
- Container for Asynclestener objects
- Starts asyncio event loop
- Manages multiple listeners

### Asynclestener
- Listens on IP:port
- Auto-detects protocols
- Routes to protocol handlers

### Config
- Used to customize listener behavior
- Contains: auth, cmd, log, policy
- Passed to protocol handlers

### Policy Rules
- Define traffic rules
- Use RouteInfo for matching
- Use ACTIONS.ALLOW or ACTIONS.DENY

### Protocols
- HTTP1O1: Web traffic
- SOCKS4: Legacy protocol
- SOCKS5: Modern protocol
- Mix them for flexibility

---

## File Templates

Each file follows this pattern:
```python
"""
Component: Purpose

Explanation of what it does and why

Key concepts and use cases
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5

def main():
    # Create configuration/listeners
    # Configure behavior
    # Create server
    # Run server

if __name__ == '__main__':
    main()
```

---

## Running Examples

All examples are self-contained and runnable:
```bash
python examples/[folder]/[file].py
```

Press Ctrl+C to stop a running example.

---

## Next Steps

1. **Test the examples** - Run each one to see how they work
2. **Modify them** - Change ports, credentials, rules
3. **Combine them** - Mix authentication + policies
4. **Create your own** - Use as templates for custom proxies

For more information, see the main README.md in the project root.
