from ..net.tunnel import Tunnel
from ..conf import Config
from ..policy import RouteInfo, NETADDRESS as IPADDR
from ..utills import integer, ipaddress, dns
from .base import BaseProtocol
from io import BytesIO

class SOCKS5(BaseProtocol): # messing GSSAPI and IANA ASSIGNED

    def __str__(self):
        """
        Return the protocol name used for identification and logging.
        """
        return 'SOCKS5'
    
    def __init__(self,config: Config | None = None):
        """
        params:
            config : Config : configuration object containing policy, auth, and command settings
        returns:
            None
        errors:
            ValueError : if configuration parameters are invalid
        """
        super().__init__(config)
        self.config = config or Config()
        self.version = 5
        self.policy = self.config.policy
        self.privatemethod = self.config.privatemethod
        self.supported_commands = self.config.cmd
        if self.config.auth.username  and self.config.auth.password:
            self.username,self.password = self.config.auth.username, self.config.auth.password ; self.authreq = True
        else:
            self.username,self.password = None,None ; self.authreq = False

    def atyp(self, atyp: int,ipOrdomain: str):
        """
        Validate address type against configuration.
        params:
            atyp : int : address type code (1 for IPv4, 3 for domain, 4 for IPv6)
            ipOrdomain : str : IP address or domain name string
        returns:
            bool : whether the address type is allowed by configuration
        errors:
            Exception : general error during address type validation
        """
        match atyp:

            case 1:
                return True if self.config.connection.ipv4.isenabled and ipaddress.isipaddress(ipOrdomain) and ipaddress.version(ipOrdomain) == 4 else False
            
            case 4:
                return True if self.config.connection.ipv6.isenabled and ipaddress.ip.isipaddress(ipOrdomain) and ipaddress.version(ipOrdomain) == 6 else False
            
            case 3:
                return True if dns.check(ipOrdomain) and self.config.connection.dns.isenabled else False
    
    async def rreply(self, buffer: bytes, tunnel: Tunnel):
        """
        params:
            buffer : bytes : the client request buffer containing SOCKS5 protocol data
            tunnel : Tunnel : the tunnel object for managing the connection
        returns:
            None
        errors:
            Exception : general error during request processing
        """
        #=================== (1) identifier/method =================== +

        request = BytesIO(buffer)
        """
        +----+----------+----------+
        |VER | NMETHODS | METHODS  |
        +----+----------+----------+
        | 1  |    1     | 1 to 255 |
        +----+----------+----------+
        """
        
        VER = request.read(1)

        if VER != b"\x05":
            tunnel.src.close() ; tunnel.record("bad version socks5 version received") ; return

        NMETHODS = integer.fromBytes(request.read(1))
        METHODS = list(request.read(NMETHODS))

        method = None

        if 0 in METHODS :
            method = 0 if not self.authreq else None

        if method is None and 2 in METHODS:
            method = 2 if self.authreq else None
        
        if method is None and 80 in METHODS:
            method = 80 if self.privatemethod else None
        #=================== (1) identifier/method =================== -

        #=================== (2) METHOD SELECTION MESSAGE =================== +
        """
        o  X'00' NO AUTHENTICATION REQUIRED
        o  X'01' GSSAPI
        o  X'02' USERNAME/PASSWORD
        o  X'03' to X'7F' IANA ASSIGNED
        o  X'80' to X'FE' RESERVED FOR PRIVATE METHODS
        o  X'FF' NO ACCEPTABLE METHODS
        """
        response = b"".join(
            [
                int(self.version).to_bytes(1,"big"),
                int(method).to_bytes(1,"big") if method is not None else b"\xFF"
            ]
        )

        await tunnel.src.sendbuffer(response, count=False)

        match method:
            case 0: # NO AUTHENTICATION REQUIRED
                pass
            
            case 2:# METHOD USERNAME/PASSWORD
                """
                +----+------+----------+------+----------+
                |VER | ULEN |  UNAME   | PLEN |  PASSWD  |
                +----+------+----------+------+----------+
                | 1  |  1   | 1 to 255 |  1   | 1 to 255 |
                +----+------+----------+------+----------+
                """
                err,response = await tunnel.src.recvbuffer() ; request = BytesIO(response)

                if err : tunnel.src.close() ; tunnel.record(str(err)) ; return
                
                VER = request.read(1)
                
                if VER != b"\x01":
                    tunnel.src.close() ; tunnel.record(f"bad auth version recvied {VER}") ; return
                
                ULEN = integer.fromBytes(
                    request.read(1)
                )

                UNAME = request.read(ULEN)
                PLEN = integer.fromBytes(
                    request.read(1)
                )

                PASSWD = request.read(PLEN)
                status = 0 if self.username == UNAME and self.password == PASSWD else 2

                """
                +----+--------+
                |VER | STATUS |
                +----+--------+
                | 1  |   1    |
                +----+--------+
                A STATUS field of X'00' indicates success. If the server returns a
                `failure' (STATUS value other than X'00') status, it MUST close the
                connection.
                """

                await tunnel.src.sendbuffer(
                    b"".join(
                        [
                            int(1).to_bytes(1,"big"),
                            int(status).to_bytes(1,"big")
                        ]
                    ),count=False
                )
                    
                if status : tunnel.src.close() ; tunnel.record(f"incorrect password recived {PASSWD} or username {UNAME}") ; return
    
            case 80:# PRIVATE METHODS
                if not await self.privatemethod(tunnel.src):# handle this part********************
                    tunnel.src.close() ; tunnel.record('private method failed') ; return
                
            case _:
                tunnel.src.close() ; tunnel.record('unsupported method') ; return
        #=================== (2) METHOD SELECTION MESSAGE =================== -

        #=================== (3) RECEVING REQUEST  =================== +
        """
        +----+-----+-------+------+----------+----------+
        |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
        +----+-----+-------+------+----------+----------+
        | 1  |  1  | X'00' |  1   | Variable |    2     |
        +----+-----+-------+------+----------+----------+

        o  CMD
             o  CONNECT X'01'
             o  BIND X'02'
             o  UDP ASSOCIATE X'03'

        o  ATYP   address type of following address
             o  IP V4 address: X'01'
             o  DOMAINNAME: X'03'
             o  IP V6 address: X'04'

        """       
        err, request = await tunnel.src.recvbuffer() ; request = BytesIO(request)

        if err : tunnel.src.close() ; tunnel.record(str(err)) ; return

        VER = request.read(1)

        if VER != b"\x05":
            tunnel.src.close() ; tunnel.record(f"bad Version recved {VER}") ; return

        CMD = integer.fromBytes(
            request.read(1)
        )
 
        RSV = request.read(1)

        if RSV != b"\x00":
            tunnel.src.close() ; tunnel.record('invalid reserved field') ; return
        
        ATYP = integer.fromBytes(
            request.read(1)
        )

        BoundAddress = tunnel.src.laddr

        DSTDOMAIN = None

        match ATYP:

            case 1:
                DSTADDR = ipaddress.unpack(request.read(4))

            case 4:
                DSTADDR = ipaddress.unpack(request.read(16))

            case 3:

                DOMLEN = integer.fromBytes(request.read(1))

                DSTDOMAIN = request.read(DOMLEN).decode()

                DSTADDR = (await self.dnsrb(DSTDOMAIN)) if dns.check(DSTDOMAIN) and self.config.connection.dns.isenabled else None

            case _:

                DSTADDR = None

        DSTPORT = integer.fromBytes(request.read(2)) if DSTADDR else 0

        if not self.atyp(ATYP,(DSTDOMAIN or DSTADDR)):
            
            response = b"".join(
                [
                        int(self.version).to_bytes(1,"big"), int(8).to_bytes(1,"big"), int(0).to_bytes(1,"big"), int(ATYP).to_bytes(1,"big"), ipaddress.pack(BoundAddress.ip), int(BoundAddress.port).to_bytes(2,"big")
                ]
            )
            await tunnel.src.sendbuffer(response,end=True,count=False) ; tunnel.record('Address type not supported') ; return
        
        if not DSTADDR:

            response = b"".join(
                [
                        int(self.version).to_bytes(1,"big"), int(4).to_bytes(1,"big"), int(0).to_bytes(1,"big"), int(ATYP).to_bytes(1,"big"), ipaddress.pack(BoundAddress.ip), int(BoundAddress.port).to_bytes(2,"big")
                ]
            )
            await tunnel.src.sendbuffer(response,end=True,count=False) ; tunnel.record('Host unreachable') ; return

            
        #=================== (3) RECEVING REQUEST  =================== -

        
        if CMD == 1 and self.supported_commands.get(CMD): # METHOD == CONNECT
            '''
            +----+-----+-------+------+----------+----------+
            |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  | X'00' |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
            o  REP    Reply field:
             o  X'00' succeeded
             o  X'01' general SOCKS server failure
             o  X'02' connection not allowed by ruleset
             o  X'03' Network unreachable
             o  X'04' Host unreachable
             o  X'05' Connection refused
             o  X'06' TTL expired
             o  X'07' Command not supported
             o  X'08' Address type not supported
             o  X'09' to X'FF' unassigned
            '''
            DST_ADDR_ROUTE = IPADDR(DSTADDR,DSTPORT,DSTDOMAIN)

            routeinfo = RouteInfo(tunnel.src.raddr,DST_ADDR_ROUTE)
            
            if not self.policy(routeinfo):
                response = b"".join(
                    [
                        int(self.version).to_bytes(1,"big"), int(2).to_bytes(1,"big"), int(0).to_bytes(1,"big"), int(ATYP).to_bytes(1,"big"), ipaddress.pack(BoundAddress.ip), int(BoundAddress.port).to_bytes(2,"big")
                    ]
                ) ; await tunnel.src.sendbuffer(response,end=True,count=False) ; tunnel.record('policy refused error') ; return

            error = await tunnel.link(
                DSTADDR,
                DSTPORT
            )

            if DSTDOMAIN:
                tunnel.dst.raddr.SetDomain(DSTDOMAIN)

            if error:

                error = error.__class__

                if error is ConnectionRefusedError:
                    replyCode = 5

                elif error is TimeoutError:
                    replyCode = 3

                else:
                    replyCode = 1

            else: # messing parts shoud be add later **********************
                replyCode = 0
                
            atyp = (1) if ipaddress.version(DSTADDR) == 4 else 4
            
            response = b"".join(
                    [
                        int(self.version).to_bytes(1,"big"), int(replyCode).to_bytes(1,"big"), int(0).to_bytes(1,"big"), int(atyp).to_bytes(1,"big"), ipaddress.pack(BoundAddress.ip), int(BoundAddress.port).to_bytes(2,"big")
                    ]
                )

            match replyCode:

                case 0:
                    await tunnel.src.sendbuffer(response,count=False)
                    await tunnel.call(180)

                case _:
                    await tunnel.src.sendbuffer(response,end=True,count=False) ; tunnel.record(f'connection to destionation error reply code {replyCode}') ; return 
            
            
        # THE END OF THE CONNECT PART

        else:
            response = b"".join(
                    [
                        int(self.version).to_bytes(1,"big"), int(7).to_bytes(1,"big"), int(0).to_bytes(1,"big"), int(ATYP).to_bytes(1,"big"), ipaddress.pack(BoundAddress.ip), int(BoundAddress.port).to_bytes(2,"big")
                    ]
                )
            await tunnel.src.sendbuffer(response,end=True,count=False) ; tunnel.record(f"in supported command") ; return