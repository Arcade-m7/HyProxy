"""Policy engine exports and helpers.

Expose `Policy`, `RouteInfo`, `IPADDR`, `IPNET`, `RULES`, and `SimpleRule`.
Comments below are example usage and notes for maintainers.
"""

from .policy import Policy
from .models import RouteInfo, ACTIONS, NETADDRESS
from .rules import SimpleRule

# if policy return True that means the connection is good
# if polciy return False that means the connection is bad a policy essue

'''Pol = Policy() hadi licanhdarlek 3Liha

rule = SimpleRule(
    channel(
        dst=IPADDR('31.13.83.174',44)
    )
)

Pol.setrule(rule)

d = channel(
    IPADDR('192.168.1.1',1968),
    IPADDR('31.13.83.174',3)
)

print(Pol(d))'''