# Config CMD Examples

This folder contains examples demonstrating the CMD (Command) configuration in HyProxy.

## What is CMD?

CMD controls which commands are allowed in the proxy. There are three specific commands:

1. **CONNECT** (Option 1)
   - Allows clients to establish connections
   - Essential for proxy operation
   - Default: Enabled

2. **BIND** (Option 2)
   - Allows clients to bind to ports
   - Used for reverse connections in SOCKS
   - Default: Enabled

3. **UDP** (Option 3)
   - Enables UDP protocol support
   - Default: Enabled

## API Overview

### Accessing Commands

```python
config = Config()

# Access individual commands
config.cmd.connect     # CONNECT command
config.cmd.bind        # BIND command
config.cmd.udp         # UDP command
```

### Controlling Commands

```python
# Enable a command
config.cmd.connect.enable()

# Disable a command (note: method is "desible" - typo in source)
config.cmd.connect.desible()

# Check if enabled
is_enabled = config.cmd.connect.isenabled

# Get command status by ID
config.cmd.get(1)  # Returns True/False for CONNECT
config.cmd.get(2)  # Returns True/False for BIND
config.cmd.get(3)  # Returns True/False for UDP
```

## Files

### 01_basic_cmd.py
Demonstrates the default state of commands. Shows how to check which commands are enabled.

```bash
python 01_basic_cmd.py
```

### 02_cmd_toggle.py
Shows how to disable specific commands for different use cases.

Example scenarios:
- Disable UDP for low-overhead proxy
- Disable BIND for security
- Disable CONNECT for monitoring-only setup

```bash
python 02_cmd_toggle.py
```

### 03_cmd_combinations.py
Combines command control with authentication for access policies.

Access tiers:
- **Admin**: All commands enabled
- **User**: Limited commands (no BIND, no UDP)
- **Guest**: Only CONNECT allowed

```bash
python 03_cmd_combinations.py
```

## Use Cases

### Security through Command Control

```python
# Admin: Full access
admin_config = Config()
# All commands enabled by default

# Guest: Limited access
guest_config = Config()
guest_config.cmd.bind.desible()
guest_config.cmd.udp.desible()
```

### Performance Optimization

```python
# UDP off for lower overhead
config = Config()
config.cmd.udp.desible()
```

### Feature Restriction

```python
# SOCKS BIND not needed
config = Config()
config.cmd.bind.desible()  # Disable reverse connections
```

## Learning Path

1. Start with **01_basic_cmd.py** - Understand default state
2. Try **02_cmd_toggle.py** - See how to control commands
3. Study **03_cmd_combinations.py** - Combine with auth for policies

## Command Properties

```python
# Check status
config.cmd.connect.isenabled  # Get boolean value

# All three commands have same interface
for cmd_name, cmd_obj in [('connect', config.cmd.connect),
                          ('bind', config.cmd.bind),
                          ('udp', config.cmd.udp)]:
    print(f"{cmd_name}: {cmd_obj.isenabled}")
```

## Notes

- Only connect command that work right now
- Multiple listeners can have different command configurations
- Commands work with all protocols (HTTP, SOCKS4, SOCKS5)
- Combining with authentication creates fine-grained access control

## Advanced Topics

See also:
- `config_auth/` for authentication combinations
- `config_log/` for logging with commands
- `config_policy/` for traffic control

## Reference

For more information about the CMD implementation, see `hyproxy/conf/cmd.py`
