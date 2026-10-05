# Config Auth Examples

Authentication configuration controls who can use the proxy.

## What is Authentication?

Authentication:
- Requires username and password
- Validates all proxy requests
- Prevents unauthorized access
- Works with all protocols

## API Overview

```python
config = Config()

# No authentication (allow all)
# (default - no setup needed)

config.auth.setusername(b'admin')
config.auth.setpassword(b'admin123')

```

## Files

### 01_no_auth.py
No authentication - allow all connections.

```bash
python 01_no_auth.py
```

Features:
- No username/password required
- Any client can connect
- Default behavior
- Fastest performance

Use Case:
- Internal networks
- Testing environments
- Trusted networks

### 02_basic_auth.py
Single authentication credentials.

```bash
python 02_basic_auth.py
```

Features:
- One username/password pair
- All clients use same credentials
- Simple setup
- Everyone has same access

Use Case:
- Small deployments
- Simple shared proxy
- Single user setup

### 03_multiple_credentials.py
Multiple user accounts with different access levels.

```bash
python 03_multiple_credentials.py
```

Features:
- Different users
- Different passwords
- Same proxy access
- User tracking

Use Case:
- Corporate environments
- Multi-user deployments
- Audit/logging needs

## Authentication Flow

```
1. Client connects
2. Client sends request with credentials
3. Proxy checks username/password
4. Match found?
   - Yes: Allow request
   - No: Deny request
5. Continue or close connection
```

## Configuration Patterns

### Allow All (No Auth)

```python
config = Config()
# No auth setup needed
```

### Single User

```python
config = Config()
config.auth.setusername(b'admin')
config.auth.setpassword(b'password')
```

### Multiple Users

```python
config = Config()
config.auth.adduser(b'admin', b'admin123')
config.auth.adduser(b'user', b'user123')
config.auth.adduser(b'guest', b'guest123')
```

## Integration with Policies

Combine auth with policies:

```python
config = Config()

# Setup authentication
config.auth.adduser(b'admin', b'admin123')
config.auth.adduser(b'user', b'user123')

# Setup policies (if admin)
config.policy.addrule(SimpleRule(
    RouteInfo(dst=NETADDRESS(port=443)),
    'Allow HTTPS',
    ACTIONS.ALLOW
))

# Both apply together
# User must authenticate AND pass policy
```

## Learning Path

1. Start with **01_no_auth.py**
2. Try **02_basic_auth.py**
3. Study **03_multiple_credentials.py**

## Security Considerations

### Password Handling
- Use strong passwords (minimum 8 characters)
- Change passwords regularly
- Never hardcode in production
- Use environment variables instead

### Authentication Options
- No auth: Fast but insecure
- Single user: Moderate security
- Multiple users: Better auditing

### Best Practices
- Enable logging with auth
- Monitor failed attempts
- Use with HTTPS/SOCKS5 (encrypted)
- Combine with IP-based policies

## Notes

- Default: No authentication (allow all)
- Auth bytes: Use `b'string'` format
- Works with all protocols
- Applies to all clients

## Reference

For implementation details, see `hyproxy/conf/auth.py`
