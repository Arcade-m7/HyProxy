from ..net.network import Stream, BytesParser 
from ..net.tunnel import Tunnel
from ..protocols import HTTP101, SOCKS4, SOCKS5

from .utils import randid
from .protocols import Protocols

from typing import List
from asyncio import CancelledError, start_server, create_task
import logging

class Asynclistener:

    def __init__(self,
            name: str|None = None,
            ip: str = '0.0.0.0',
            port: int = 1968,
            protocols: List[HTTP101|SOCKS5|SOCKS4] = [HTTP101(),SOCKS5(),SOCKS4()],
        ): # add support ssl or not 
        """
        Create an asynchronous listener bound to an IP and port.
        params:
            name : str|None : optional listener name
            ip : str : bind address
            port : int : bind port
            protocols : list : list of protocol classes to support
        returns:
            None
        errors:
            Exception : if provided parameters are invalid
        """
        self.ip, self.port, self.protocols = ip, port, protocols
        self.name = name or randid()

        log = logging.Logger(name)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler = logging.StreamHandler()

        handler.setLevel(logging.DEBUG)

        handler.setFormatter(formatter)

        log.addHandler(
            handler
        )
        self.log = log
        
        self.Sprotocol = Protocols.add(protocols)

    def wraper(self, clientreader, clientwriter):
        """
        Wrap accepted socket streams into a `Stream` and hand off to the filter.
        params:
            clientreader : asyncio.StreamReader : reader from accepted socket
            clientwriter : asyncio.StreamWriter : writer from accepted socket
        returns:
            coroutine : the filter coroutine for the connected stream
        errors:
            Exception : on Stream construction failure
        """
        return self.filter(Stream(clientreader, clientwriter))
    
    def setlogger(self, logger: logging.Logger):
        assert type(logger) is logging.Logger
        self.log = logger
                
    async def filter(self, stream: Stream):
        """
        Inspect the client's initial bytes to detect protocol and create a Tunnel.
        params:
            stream : Stream : incoming client stream
        returns:
            None
        errors:
            None
        """
        
        error,buffer = await stream.recvbuffer(buffersize=1024,count=False)
        if error : stream.close() ; return
        
        Pname = BytesParser(buffer) # protocol name

        protocole = self.Sprotocol.get(Pname)

        if not protocole:
            stream.close() ; return
        
        config = protocole.config
      
        tunnel = Tunnel.tunnel(
            stream,
            config,
            str(protocole),
            self.name
        )

        try:
            await protocole.reply(
                buffer,
                tunnel
            )
        except Exception as er:
            self.log.exception('error')
        finally:
            stream.close()

    async def getready(self):
        """
        Start the asyncio TCP server bound to the configured address.
        params:
            None
        returns:
            None
        errors:
            Exception : if server cannot be started
        """
        self.server = await start_server(
            self.wraper,
            host=self.ip,
            port=self.port
        )

    async def serv(self):
        """
        Start serving incoming connections until cancelled.
        params:
            None
        returns:
            None
        errors:
            Exception : server runtime errors
        """
        await self.getready()
        self.log.info(f'server {self.name} is running on {self.ip}:{self.port}')
        try:
            await self.server.serve_forever()
        except CancelledError:
            pass

    def stop(self):
        """
        Stop the running server and wait for it to close.
        params:
            None
        returns:
            None
        errors:
            Exception : if server closure fails
        """
        self.server.close()