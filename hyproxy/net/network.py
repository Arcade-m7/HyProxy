from ..policy import NETADDRESS as IPADDR

from asyncio import StreamReader, StreamWriter, wait_for

def BytesParser(buffer: bytes):
    """Detect protocol by first byte of client data.

    For first byte 0x04 => SOCKS4
    For first byte 0x05 => SOCKS5
    Otherwise => HTTP.
    """
    if buffer and (version:=buffer[0]) in [4,5]:
        return 'SOCKS4' if version == 4 else 'SOCKS5'
    return 'HTTP'

async def forwardfunction(tunnel, timeout: int | float):
    """
    Wrapper that forwards data for the given tunnel.
    params:
        tunnel : Tunnel : tunnel to forward
        timeout : int|float : forwarding timeout
    returns:
        None
    errors:
        Exception : from tunnel.forward
    """
    await tunnel.forward(timeout)

class Stream:
    """Wrapper for asyncio StreamReader/StreamWriter with counters and timeout."""

    def __init__(self,clientreader: StreamReader, clientwriter: StreamWriter, timeout: float|int = 60):
        """
        params:
            clientreader : StreamReader : asyncio stream reader
            clientwriter : StreamWriter : asyncio stream writer
            timeout : float|int : timeout for operations
        returns:
            None
        errors:
            Exception : general error during initialization
        """
        self.reader = clientreader ; self.writer = clientwriter
        self.__timeout = timeout ; self.__ds, self.__dr = 0,0
        self.sock = self.writer.get_extra_info('socket')
        self.raddr = self.__raddr__() ; self.laddr = self.__laddr__()
            
    async def sendbuffer(self,buffer: bytes, end: bool = False, count: bool = True):
        """
        Send bytes to peer and optionally close connection.
        params:
            buffer : bytes : data to send
            end : bool : whether to close connection after sending
            count : bool : whether to count bytes sent
        returns:
            None or Exception : None on success or exception on failure
        errors:
            Exception : write or drain failure
        """
        try:
            self.writer.write(buffer)
            await self.writer.drain()
            self.__ds += len(buffer) if count else 0
            if end:
                self.writer.close()
            return None
        except Exception as er:
            return er

    async def recvbuffer(self, buffersize: int = 60000,count: bool = True):
        """
        Read up to buffersize bytes with timeout.
        params:
            buffersize : int : maximum bytes to read
            count : bool : whether to count bytes received
        returns:
            tuple : (error, buffer) where error is None/Exception and buffer is bytes
        errors:
            TimeoutError : if timeout expires
            Exception : read failure
        """
        try:
            recvedbuffer = await wait_for(self.reader.read(buffersize),self.__timeout) ; self.__dr += len(recvedbuffer) if count else 0
            return None, (recvedbuffer)
        except Exception as er:
            return er, None
        
    async def recvuntil(self, sep: bytes,count: bool = True):
        """
        Read bytes until separator is found with timeout.
        params:
            sep : bytes : separator to read until
            count : bool : whether to count bytes received
        returns:
            tuple : (error, buffer) where error is None/Exception and buffer is bytes
        errors:
            TimeoutError : if timeout expires
            Exception : read failure
        """
        try:
            recvedbuffer = await wait_for(self.reader.readuntil(sep),self.__timeout) ; self.__dr += len(recvedbuffer) if count else 0
            return None, (recvedbuffer)
        except Exception as er:
            return er, None
        
    async def drain(self):
        """
        Wait until write buffer is flushed.
        params:
            None
        returns:
            None
        errors:
            Exception : drain failure
        """
        await self.writer.drain()

    async def read(self, count: bool = True,timeout: int|float = 60.0):
        """
        Read data from stream with timeout.
        params:
            *args : any : arguments for reader.read
            count : bool : whether to count bytes
            timeout : int|float : read timeout
            **kwds : any : keyword arguments for reader.read
        returns:
            bytes : data read
        errors:
            TimeoutError : if timeout expires
            Exception : read failure
        """
        for _ in range(1,timeout + 1):
            buffer = await wait_for(self.reader.read(60000), 1)
            if buffer:
                self.__dr += len(buffer) if count else 0 ; return buffer
    
    async def wait_closed(self):
        """
        Wait until the stream is fully closed.
        params:
            None
        returns:
            None
        errors:
            Exception : wait failure
        """
        await self.writer.wait_closed()
    
    def write(self,buffer: bytes, count : bool = True):
        """
        Write bytes to the stream buffer (non-blocking).
        params:
            buffer : bytes : data to write
            count : bool : whether to count bytes sent
        returns:
            None
        errors:
            None
        """
        self.writer.write(buffer)
        self.__ds += len(buffer) if count else 0
    
    def settimeout(self,time: int|float):
        """
        Set the timeout value for stream operations.
        params:
            time : int|float : timeout value in seconds
        returns:
            None
        errors:
            ValueError : if time is not int or float
        """
        if isinstance(time,(int,float)):
            self.__timeout = time
        else:
            raise ValueError('the type of time must be int or float')
        
    def gettimeout(self):
        """
        Get the current timeout value.
        params:
            None
        returns:
            float : current timeout value
        errors:
            None
        """
        return self.__timeout
    
    def datasent(self):
        """
        Get the total number of bytes sent.
        params:
            None
        returns:
            int : total bytes sent
        errors:
            None
        """
        return self.__ds
    
    def datarecv(self):
        """
        Get the total number of bytes received.
        params:
            None
        returns:
            int : total bytes received
        errors:
            None
        """
        return self.__dr
    
    def close(self):
        """
        Close the stream connection.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.writer.close()
    
    def __laddr__(self):
        """
        Get the local address of the stream.
        params:
            None
        returns:
            IPADDR : local address
        errors:
            Exception : socket error
        """
        return IPADDR(
            * self.sock.getsockname(),None
        )
    
    def __raddr__(self):
        """
        Get the remote address of the stream.
        params:
            None
        returns:
            IPADDR : remote address
        errors:
            Exception : socket error
        """
        return IPADDR(
            * self.sock.getpeername(),None
        )        

