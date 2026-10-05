from ..policy import NETADDRESS as IPADDR 
from dataclasses import dataclass
from time import time
from uuid import uuid4

@dataclass
class CONNECTIONINFO:

    uuid    : str
    stime   : int|float
    etime   : int|float
    lname   : str
    protocol: str
    srcaddr : IPADDR
    dstaddr : IPADDR
    datas   : int
    datar   : int
    error   : str = None

class ConnectionInfo:

    def __init__(self,tunnel):
        self.stime = time()
        self.tunnel = tunnel

    def record(self,error=None):
        """Generate a traffic summary object for this tunnel connection."""
        summary = CONNECTIONINFO(
            uuid4().hex,
            self.stime,
            time(),
            self.tunnel.lname,
            self.tunnel.prot,
            self.tunnel.src.raddr,
            self.tunnel.dst.raddr if self.tunnel.dst else  None,
            self.tunnel.src.datasent(),
            self.tunnel.dst.datarecv() if self.tunnel.dst else 0,
            error
        )
        return summary