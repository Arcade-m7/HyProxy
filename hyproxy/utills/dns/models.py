from dataclasses import dataclass

@dataclass
class Table:
    ip : str
    tte: float # time to expire

class Cache(dict):

    def add(self, key: str, value: Table):
        self.update(
            {
                key: value
            }
        )

class DnsCache:

    ipv4 = Cache()
    ipv6 = Cache()

    @classmethod
    def addtocache(cls, qtype: str, ip: str, domain: str, tte: float|int):
        ipcache = cls.ipv4 if qtype == 'A' else cls.ipv6
        ipcache.add(
            domain, Table(ip, tte)
        )

    @classmethod
    def getfromcache(cls, qtype: str, domain: str):
        ipcache = cls.ipv4 if qtype == 'A' else cls.ipv6
        return ipcache.get(domain)