from ..utills import dns
from ..conf import Config


class BaseProtocol:

    def __init__(self, config: Config):
        """
        Initialize the protocol handler with configuration.
        params:
            config : Config : configuration object
        returns:
            None
        errors:
            Exception : if config is invalid
        """
        self.config = config

    async def reply(self, *args,**kwd):
        """
        Dispatch request handling with optional async context manager.
        params:
            *args : any : arguments to pass to rreply
            **kwd : any : keyword arguments to pass to rreply
        returns:
            result from rreply
        errors:
            Exception : from rreply or async context
        """
        if not self.config.connection.sameas:
            return await self.rreply(*args,**kwd)
        async with self.config.connection.sameas:
            return await self.rreply(*args,**kwd)
        
    async def dns(self, dn: str, version: int = 4):
        """
        Resolve domain name to IP address.
        params:
            dn : str : domain name to resolve
            version : int : IP version (4 for IPv4, 6 for IPv6)
        returns:
            str or None : resolved IP address or None if resolution not allowed
        errors:
            Exception : general error during DNS resolution
        """
        qtype = 'AAAA' if version == 6 else 'A'
        match version:
            case 4:
                return await dns.resolve(dn,qtype)
            case 6:
                return await dns.resolve(dn,qtype)
            
    async def dnsrb(self,domain: str):
        """
        Resolve domain name with fallback between IPv6 and IPv4.
        params:
            domain : str : domain name to resolve
        returns:
            str or None : resolved IP address or None if not found
        errors:
            Exception : general error during DNS resolution
        """
        if not dns.check(domain):
            return None
        
        answer = None

        if self.config.connection.ipv6.isenabled:
            answer =  await self.dns(domain,6)
            
        if self.config.connection.ipv4.isenabled and not answer:
            answer =  await self.dns(domain,4)

        return answer