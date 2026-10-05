from ...policy import RouteInfo, NETADDRESS as IPADDR
from ...net.tunnel import Tunnel
from ...conf import Config
from ...utills import ipaddress
from ..base import BaseProtocol

from .parser import REQUEST, RESPONSE

from urllib.parse import urlsplit
from base64 import b64encode

CRLF = b"\r\n\r\n"

class HTTP101(BaseProtocol):

    def __str__(self):
        """
        Return the protocol name string for identification.
        params:
            None
        returns:
            str : protocol name
        errors:
            None
        """
        return 'HTTP'

    def __init__(self,config: Config = None):
        """
        Initialize the HTTP/1.1 protocol handler with optional config.
        params:
            config : Config|None : optional configuration
        returns:
            None
        errors:
            Exception : if configuration is invalid
        """
        super().__init__(config or Config())
        self.version = b"HTTP/1.1"
        self.policy = self.config.policy
        self.auth = b64encode(self.config.auth.username + b":" + self.config.auth.password) if self.config.auth.username and self.config.auth.password else None
        self.authreq = True if self.auth else False

    async def connect(self,request: REQUEST, tunnel: Tunnel):
        """
        Handle an HTTP CONNECT request by establishing a TCP tunnel to the target.
        params:
            request : REQUEST : parsed CONNECT request
            tunnel : Tunnel : tunnel object for the connection
        returns:
            None
        errors:
            Exception : various errors during connect handling
        """

        if b":" not in request.requesturi:
            tunnel.src.close() ; tunnel.record('invalid request URI') ; return
        
        HOSTNAME, PORT = request.requesturi.split(b":",1); HOSTNAME = HOSTNAME.decode()
        PORT = int(PORT) ; IP = HOSTNAME if ipaddress.isipaddress(HOSTNAME) else (await self.dnsrb(HOSTNAME))

        if IP is None:
            response = RESPONSE(
                self.version,
                b"502",
                b"Bad Gateway",
                {b"Content-Type": b"text/plain"},
                b"502 Bad Gateway: Unable to resolve destination hostname."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('dns resolution error') ; return

        routeinfo = RouteInfo(
            tunnel.src.raddr,
            IPADDR(
                IP,
                PORT,
                HOSTNAME if HOSTNAME != IP else None
            )
        )


        if not self.policy(routeinfo):
            response = RESPONSE(
                self.version,
                b"403",
                b"Forbidden",
                {b"Content-Type": b"text/plain"},
                b"403 Forbidden: Access is denied."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('policy refused') ; return
        
        error = await tunnel.link(IP, PORT)

        if error:

            response = RESPONSE(
                self.version,
                b"502",
                b"Bad Gateway",
                {b"Content-Type": b"text/plain"},
                b"502 Bad Gateway: Unable to connect to destination."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('connection failed') ; return
        
        response = RESPONSE(
            self.version,
            b"200",
            b"Connection Established",
            {b"Content-Type": b"text/plain"},
        )
        
        tunnel.dst.raddr.SetDomain(HOSTNAME) if HOSTNAME != IP else None
        await tunnel.src.sendbuffer(response.compose()) ; await tunnel.call(timeout=120)

    async def othermethod(self,request: REQUEST, tunnel: Tunnel):
        """
        Forward non-CONNECT HTTP methods to destination server.
        params:
            request : REQUEST : parsed HTTP request
            tunnel : Tunnel : tunnel for the connection
        returns:
            None
        errors:
            Exception : on request processing errors
        """
        urlsp = urlsplit(request.requesturi.decode())

        PORT, HOSTNAME = urlsp.port if urlsp.port else (443 if urlsp.scheme == "https" else 80), urlsp.hostname
        IP = (await self.dnsrb(HOSTNAME)) if not ipaddress.isipaddress(HOSTNAME) else HOSTNAME

        if ( 1 <= PORT <= 65535 ) is False:
            response = RESPONSE(
                self.version,
                b"400",
                b"Bad Request",
                {b"Content-Type": b"text/plain"},
                b"400 Bad Request: Invalid port number."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('invalid port') ; return

        if IP is None:
            response = RESPONSE(
                self.version,
                b"502",
                b"Bad Gateway",
                {b"Content-Type": b"text/plain"},
                b"502 Bad Gateway: Unable to resolve destination hostname."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('dns resolution error') ; return

        routeinfo = RouteInfo(
            tunnel.src.raddr,
            IPADDR(
                IP,
                PORT,
                HOSTNAME if HOSTNAME != IP else None
            )
        )
        if not self.policy(routeinfo):
            response = RESPONSE(
                self.version,
                b"403",
                b"Forbidden",
                {b"Content-Type": b"text/plain"},
                b"403 Forbidden: Access is denied."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('policy refused') ; return
        
        error = await tunnel.link(IP,PORT)
        if error:
            response = RESPONSE(
                self.version,
                b"502",
                b"Bad Gateway",
                {b"Content-Type": b"text/plain"},
                b"502 Bad Gateway: Unable to connect to destination."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True, count=False) ; tunnel.record('connection failed') ; return
        
        request.headers[b"Host"] = HOSTNAME.encode()

        tunnel.dst.raddr.SetDomain(HOSTNAME) if HOSTNAME != IP else None

        request.requesturi = (urlsp.path.encode() if urlsp.path else b"/") + (b"?" + urlsp.query.encode() if urlsp.query else b"") + (b"#" + urlsp.fragment.encode() if urlsp.fragment else b"")

        await tunnel.dst.sendbuffer(request.compose())

        await tunnel.call(timeout= 60*5 if request.headers.get(b"Connection",b"").lower() == b"keep-alive" else 120)

    async def rreply(self,raw: bytes,tunnel: Tunnel):
        """
        Parse the initial raw client bytes and dispatch to CONNECT or other handlers.
        params:
            raw : bytes : initial raw buffer from client
            tunnel : Tunnel : tunnel object
        returns:
            None
        errors:
            Exception : if parsing or processing fails
        """

        if CRLF not in raw:
            err,buffer = await tunnel.src.recvuntil(CRLF,count=False)
            if err: tunnel.src.close() ; tunnel.record('failed to receive request');return
            raw += buffer

        try:
            request = REQUEST.HTTPParser(raw)
        except Exception as er :
            tunnel.src.close() ; tunnel.record('failed to parse request') ; return
        
        if self.authreq and not (authinfo:=request.headers.get(b"Proxy-Authorization")):
            response = RESPONSE(
                self.version,
                b"407",
                b"Proxy Authentication Required",
                {
                    b"Content-Type": b"text/plain",
                    b"Proxy-Authenticate": b'Basic realm="EZProxy"'
                },
                b"407 Proxy Authentication Required: Authentication is required to access this proxy."
            )
            await tunnel.src.sendbuffer(response.compose(), end=True) ; tunnel.record('authentication required') ; return
        
        if self.authreq:
            authtype, auth = authinfo.split(b" ",1)

            if authtype.lower() != b"basic":
                response = RESPONSE(
                    self.version,
                    b"400",
                    b"Bad Request",
                    {b"Content-Type": b"text/plain"},
                    b"400 Bad Request: Unsupported authentication type."
                )
                await tunnel.src.sendbuffer(response.compose(), end=True) ; tunnel.record('unsupported authentication type') ; return
            
            if auth != self.auth:
                response = RESPONSE(
                    self.version,
                    b"407",
                    b"Proxy Authentication Required",
                    {
                        b"Content-Type": b"text/plain",
                        b"Proxy-Authenticate": b'Basic realm="EZProxy"'
                    },
                    b"407 Proxy Authentication Required: Invalid credentials."
                )
                await tunnel.src.sendbuffer(response.compose(), end=True) ; tunnel.record('invalid credentials') ; return

        match request.method:

            case b"CONNECT":
                await self.connect(request,tunnel)

            case _:
                await self.othermethod(request,tunnel)