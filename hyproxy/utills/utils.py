from socket import inet_aton, inet_ntoa
from ipaddress import ip_address


class ipaddress:
    """IP address utilities for parsing and packing/repacking wire format."""

    @classmethod
    def isipaddress(cls,ip):
        """Return True if string is valid IPv4 or IPv6 address."""
        try:
            ip = ip_address(ip)
            return True
        except:
            return False

    @classmethod
    def pack(cls,ip):
        """Return 4-byte packed IPv4 address usable in SOCKS messages."""
        return inet_aton(str(ip)) if cls.isipaddress(ip) else None

    @classmethod
    def unpack(cls,ip):
        """Convert 4-byte packed IPv4 to text address string."""
        return inet_ntoa(ip)  if cls.isipaddress(ip) else None
        
    @classmethod
    def version(cls,ip):
        """Return IP version number 4 or 6."""
        if cls.isipaddress(ip):
            return ip_address(ip).version
        raise ValueError
        
class integer:
    """Convenience wrapper around integer conversion helpers."""
        
    @staticmethod
    def fromBytes(n,*args,**keys):
        """Safe `int.from_bytes` conversion, returning None on failure."""
        try:
            return int.from_bytes(n,*args,**keys)
        except:
            return None