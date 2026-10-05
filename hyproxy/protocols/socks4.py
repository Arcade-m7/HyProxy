from ..policy import RouteInfo, NETADDRESS as IPADDR
from ..conf import Config
from ..net.tunnel import Tunnel
from ..utills import integer, ipaddress, dns
from .base import BaseProtocol
from io import BytesIO

class SOCKS4(BaseProtocol):

    def __str__(self):
        """
        Return the protocol name for identification.
        params:
            None
        returns:
            str : protocol name identifier
        errors:
            None
        """
        return 'SOCKS4'

    def __init__(
            self,
            config: Config | None = None
        ):
        """
        params:
            config : Config : configuration object containing policy and auth settings
        returns:
            None
        errors:
            TypeError : if userid is not a bytes or None
        """
        super().__init__(config or Config())
        self.version = 4
        self.policy = self.config.policy
        self.supported_commands = self.config.cmd
        self.userid = self.config.auth.username

        
    async def rreply(self, buffer: bytes, tunnel: Tunnel):
        """
        params:
            buffer : bytes : the client request buffer containing SOCKS4 protocol data
            tunnel : Tunnel : the tunnel object for managing the connection
        returns:
            None
        errors:
            Exception : general error during request processing
        """
        # Wrap raw bytes in BytesIO for sequential parsing.
        request = BytesIO(buffer)

        # SOCKS4 version must be 0x04.
        VN = request.read(1)
        if VN != b"\x04":
            tunnel.src.close(); tunnel.record('invalid version number') ; tunnel.record(f"invalid verssion recived {VN}") ; return

        # Command code: 1=CONNECT, 2=BIND (unsupported in this implementation).
        CD = integer.fromBytes(request.read(1))

        # Destination port is 2 bytes, network byte order.
        DSTPORT = integer.fromBytes(request.read(2))

        # Next 4 bytes are destination IP in network order.
        DSTIP = ipaddress.unpack(request.read(4))

        # Basic validation: valid IP string and port integer.
        if not all([ipaddress.isipaddress(DSTIP), type(DSTPORT) is int , DSTPORT in range(0, 65536)]):
            tunnel.src.close(); tunnel.record('invalid data sent') ; tunnel.record(f"invalid data type recived") ; return

        # USERID is variable length and NUL-terminated.
        USERID = request.read()[:-1]; USERID = USERID if USERID else None

        if self.userid and self.userid != USERID:
        
            buffer = b"".join(
                [
                    int(0).to_bytes(1,'big'),
                    int(93).to_bytes(1,'big'),
                    int(0).to_bytes(2,'big'),
                    ipaddress.pack(DSTIP),
                ]
            )
            await tunnel.src.sendbuffer(buffer, count=False, end=True) ; tunnel.record('connection refused because client send different userid') ; return
        
        # THIS PART FOR HANDLING THE CONNECT COMMAND 

        if CD == 1 and self.supported_commands.get(CD):

            # Build policy route and evaluate via policy engine.
            routeinfo = RouteInfo(
                tunnel.src.raddr,
                IPADDR(DSTIP, DSTPORT),
            )

            if self.policy(routeinfo):
                # Attempt connection to destination; error indicates reject.
                error = await tunnel.link(DSTIP, DSTPORT)
                CD = 91 if error else 90
            else:
                CD = 91

            buffer = b"".join(
                        [
                            int(0).to_bytes(1,'big'),
                            int(CD).to_bytes(1,'big'),
                            int(DSTPORT).to_bytes(2,'big'),
                            ipaddress.pack(DSTIP),
                        ]
                    )
            
            match CD:
                case 90:
                    await tunnel.src.sendbuffer(buffer, count=False)
                    await tunnel.call(timeout=120)

                case 91:
                    await tunnel.src.sendbuffer(buffer, end=True, count=False)
                    tunnel.record('destination unreachable or policy blocked')
                    return

        # Unsupported commands are closed.
        else:
            await tunnel.src.sendbuffer(b"".join(
                [
                    int(0).to_bytes(1,'big'),
                    int(91).to_bytes(1,'big'),
                    int(0).to_bytes(2,'big'),
                    ipaddress.pack(DSTIP),
                ]
            ), end=True, count=False)
        
        # THIS PART FOR HANDLING THE BIND COMMAND
        """elif commandcode == 2 and self.support_commands.get(commandcode): #here should be the bind command. coming soon
            pass"""