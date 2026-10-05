from .models import Config
from .network import Stream
from .const import ConnectionInfo

from asyncio import gather, open_connection

class Tunnel: # add -----------------***************************wraper
    """Association of source/destination Streams for proxy tunnel relay."""

    def __init__(self,Src: Stream, config: Config, Dst: Stream | None = None ,prot: str = None, lname: str = None):
        """
        params:
            Src : Stream : source stream
            Dst : Stream|None : destination stream
            prot : str : protocol name
            lname : str : listener name
        returns:
            None
        errors:
            Exception : general error during initialization
        """
        self.src , self.dst = Src,Dst
        self.prot, self.lname = prot, lname
        self.config = config
        self.history = ConnectionInfo(self)
        self.func = config.call

    def setfunc(self,func):
        """
        Set the function to be invoked by tunnel call method.
        params:
            func : callable : function to be invoked by `call`
        returns:
            None
        errors:
            Exception : if func is not callable
        """
        if not callable(func):
            raise ValueError('func must be callable')
        self.func = func
    
    def record(self,error=None):
        """
        Log a summary of the tunnel connection.
        params:
            error : str|None : optional error description
        returns:
            None
        errors:
            Exception : if logging fails
        """
        coninfo = self.config.log.format(self.history.record(error=error))
        self.config.log.info(
            str(coninfo)
        ) if not error else self.config.log.warning(
            str(coninfo)
        )

    async def link(self,host: str, port: int, timeout: int|float = None, **keys: dict):
        """
        Open a TCP connection to destination host and attach remote stream.
        params:
            host : str : destination host
            port : int : destination port
            timeout : int|float|None : connection timeout
        returns:
            None or Exception : None on success or exception instance on failure
        errors:
            Exception : connection failure
        """
        try:
            timeout = timeout or self.config.connection.timeout
            re,wr = await open_connection(host=host,port=port,**keys) ; self.dst = Stream(re,wr,timeout)
        except Exception as er:
            return er

    async def __forward__(self, reader: Stream, writer: Stream, timeout: int|float = None):
        """
        Forward data from reader to writer until EOF or error.
        params:
            reader : Stream : source stream
            writer : Stream : destination stream
            timeout : int|float|None : read timeout
        returns:
            None or Exception : None on graceful close or exception instance
        errors:
            Exception : read/write errors
        """
        try:
            timeout = timeout or self.config.connection.timeout
            while (data:= await reader.read(timeout=timeout)):
                writer.write(data); 
                await writer.drain()
            writer.close() ; await writer.wait_closed() ; return     
        except Exception as er:
            writer.close() ; return er
        
    async def forward(self, time: int|float = None):
        """
        Establish bidirectional data relay between source and destination.
        params:
            time : int|float|None : per-direction timeout
        returns:
            None
        errors:
            Exception : if forwarding fails
        """
        await gather(
            *[
                self.__forward__(
                    self.src,
                    self.dst,
                    time
                ),
                self.__forward__(
                    self.dst,
                    self.src,
                    time
                )
            ]
        )
        self.record()

    async def call(self, timeout: int | float):
        """
        Invoke the configured function with this tunnel.
        params:
            timeout : int|float : call timeout passed to configured function
        returns:
            None
        errors:
            Exception : if the configured function raises
        """
        await self.func(self,timeout)

    @staticmethod
    def tunnel(src: Stream, config: Config, protocol: str = "", lname: str = ""):
        """
        Factory method that creates and returns a Tunnel instance.
        params:
            src : Stream : source stream
            config : Config : configuration to use
            protocol : str : protocol name
            lname : str : listener name
        returns:
            Tunnel : newly constructed Tunnel instance
        errors:
            Exception : if construction fails
        """
        tunnel = Tunnel(Src=src,config=config,prot=protocol,lname=lname)
        return tunnel