from .dns import resolve, resolveboth, garbageCollector, check, setttl, setnameservers
from .dns import NAMESERVER, TTL

from ...event import Event

Event.addevent(
    garbageCollector()
)