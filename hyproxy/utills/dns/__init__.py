from .dns import resolve, resolveboth, garbageCollector, check
from .dns import NAMESERVER, TTL

from ...event import Event

Event.addevent(
    garbageCollector()
)