from ipaddress import ip_address,ip_network
from re import findall
from ipaddress import IPv4Address,IPv6Address
from enum import Enum


def isip(ip):
    funcs = [ip_address,ip_network]
    for func in funcs:
        try:
            func(ip)
            return True
        except:
            pass
    return False

def wrapip(ip):
    funcs = [ip_address,ip_network]
    for func in funcs:
        try:
            return func(ip)
        except:
            pass

class ACTIONS(Enum):
    ALLOW:  int  = 1
    DENY :  int  = 0

class IP:

    def __init__(self, ip: str):
        assert isip(ip)
        self.ip = wrapip(ip)

    def __eq__(self, value):
        if type(self.ip) in [IPv4Address,IPv6Address]:
            return value.ip == self.ip
        return value.ip in self.ip
    
    def __repr__(self):
        return self.ip
    
    def __str__(self):
        return str(self.ip)
        
class DOMAIN:

    def __init__(self,domain: str):
        self.domain = domain
    
    def __eq__(self, value):
        search = findall(self.domain,value.domain)
        return value.domain in search
    
    def __repr__(self):
        return self.domain

class PORT:

    def __init__(self, port: int|range):
        self.port = port

    def __eq__(self, value):
        if type(self.port) is int:
            return value == self.port
        elif type(self.port) in [range, list]:
            return value in self.port
        else:
            return True
        
    def __repr__(self):
        return self.port
    
    def __str__(self):
        return str(self.port)
    
    def __int__(self):
        return self.port

class NETADDRESS:

    def __init__(
            self,
            ip: IPv4Address|IPv6Address|str = None,
            port: range|int|list = None,
            domain: str = None
            
        ):
        """
        params:
            ip : IPv4Address|IPv6Address|str : the IP address
            port : int : the port number
            domain : str : the domain name
        returns:
            None
        errors:
            ValueError : if ip is not a valid address type
        """
        if not any([isip(ip) , ip is None]):
            raise ValueError(f"ip must ip a str, IPv4address or IPV6address {ip}")
        
        self.ip = IP(ip) if ip else None

        self.domain = DOMAIN(domain) if type(domain) is str else None
        
        assert port is None or type(port) in [int,range,list], f"port must be int, range or list {port}"
        self.port = PORT(port)

    def __eq__(self, value):
        return all(
            [
                (self.ip == value.ip) if self.ip else True,
                (self.domain == value.domain) if self.domain  else True,
                (self.port == value.port) if self.port else True
            ]
        )
    
    def __repr__(self):
        return f"{self.domain}:{self.ip}:{self.port}"
    
    def SetIP(self,ip):
        assert isip(ip), ''
        self.ip = IP(ip)

    def SetDomain(self,domain):
        assert type(domain) is str, ""
        self.domain = DOMAIN(domain)
        

class RouteInfo:

    def __init__(
            self,
            src: NETADDRESS = None,
            dst: NETADDRESS = None
        ):
        """
        params:
            src : IPADDR : source address or network
            dst : IPADDR : destination address or network
        returns:
            None
        errors:
            Exception : general error during initialization
        """
        self.src = src
        self.dst = dst

    def __eq__(self, value):
        return all(
            [
                (self.src == value.src) if self.src else True,
                (self.dst == value.dst) if self.dst else True
            ]
        )
    
    def __repr__(self):
        return f"RouteInfo(src={repr(self.src)}, dst={repr(self.dst)})"
