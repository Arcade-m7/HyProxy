from .models import DnsCache
from .utils import isipaddress

from aiodns import DNSResolver
from re import match
from asyncio import Lock, sleep, gather
from time import time

__Lock = Lock()

TTL = 3 * 60
NAMESERVER = ['8.8.8.8','1.1.1.1']

async def resolve(domain: str, qtype: str):
    ip = DnsCache.getfromcache(qtype, domain)
    if ip:
        return ip

    adns = DNSResolver(NAMESERVER)
    async with __Lock:
        try:
            result = await adns.query_dns(domain,qtype)
            for record in result.answer:
                if hasattr(record.data,'addr') and isipaddress(record.data.addr):
                    ip = record.data.addr
                    DnsCache.addtocache(qtype, domain, ip, time() + TTL)
                    return ip
        except Exception as er:
            raise er

async def resolveboth(domain):
    return await gather(
        *[
            resolve('A' ,domain),
            resolve('AAAA', domain)
        ]
    )

async def garbageCollector():
    while True:
        await sleep(TTL)
        for ipcache in [DnsCache.ipv4, DnsCache.ipv6]:
            for domain, table in ipcache.items():
                if table.tte >= time():
                    ipcache.pop(domain)

def check(domain):
    """
    Validate a hostname using a conservative regular expression.
    params:
        domain : str : domain name to validate
    returns:
        re.Match|None : match object when domain valid else None
    errors:
        None
    """
    return match(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$", domain)

    