from asyncio import Semaphore
from socket import has_ipv6


class base:

    def __init__(self):
        """
        Initialize a base connection feature toggler as enabled.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def enable(self):
        """
        Enable this feature.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True
        
    def disable(self):
        """
        Disable this feature.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = False

class dns(base):

    def __init__(self):
        """
        DNS feature toggler (inherits enable/disable semantics).
        """
        super().__init__()

class ipv6(base):

    def __init__(self):
        """
        IPv6 feature toggler initialized disabled by default on many systems.
        """
        super().__init__()
        self.disable()

    def enable(self):
        """
        Enable IPv6 support if the platform supports it.
        raises IOError when the OS lacks IPv6 support.
        """
        if has_ipv6:
            self.isenabled = True
        else:
            raise IOError("IPv6 is not supported on this system")
        

class ipv4(base):

    def __init__(self):
        """
        IPv4 feature toggler (enabled by default).
        """
        super().__init__()

class __connection__:
    
    def __init__(self):
        """
        Container for connection-related configuration options.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.max_connections = None
        self.sameas = None
        self.timeout = 60
        self.ipv4 = ipv4()
        self.ipv6 = ipv6()
        self.dns = dns()

    def setmaxconnections(self,number):
        """
        Set maximum concurrent connections and update the semaphore.
        params:
            number : int|None : maximum concurrent connections or None to disable limit
        returns:
            None
        errors:
            AssertionError : if number is not int or None
        """
        assert type(number) in [int,None]
        self.max_connections = number
        self.sameas = Semaphore(number) if number else None
    
    def settimeout(self,seconds):
        """
        Set default connection timeout in seconds.
        params:
            seconds : int|float : timeout value in seconds
        returns:
            None
        errors:
            AssertionError : if seconds is not int or float
        """
        assert type(seconds) in [int,float]
        self.timeout = seconds