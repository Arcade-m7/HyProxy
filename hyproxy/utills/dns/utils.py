from ipaddress import ip_address

def isipaddress(ip: str) -> bool:
    try:
        ip_address(ip); return True
    except:
        return False