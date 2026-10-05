from ..net.const import CONNECTIONINFO
import logging

class StreamOutput(logging.StreamHandler):

    def __init__(self,other: logging.Logger,stream = None):
        super().__init__(stream)
        self.__other = other
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        self.setFormatter(formatter)
        """
        Initialize the stream output handler formatting log records for the given logger.
        params:
            other : logging.Logger : logger to attach to
            stream : optional stream for handler
        returns:
            None
        errors:
            Exception : if initialization fails
        """

    def reinit(self,stream = None):
        """
        Reinitialize the handler, optionally changing its output stream.
        params:
            stream : optional stream to reinitialize the handler with
        returns:
            None
        errors:
            Exception : if reinitialization fails
        """
        self.__init__(self.__other,stream)

    def enable(self):
        """
        Attach this handler to the underlying logger so records are emitted to the stream.
        params:
            None
        returns:
            None
        errors:
            Exception : if adding handler fails
        """
        self.__other.addHandler(
            self
        )

    def disable(self):
        """
        Remove this handler from the underlying logger.
        params:
            None
        returns:
            None
        errors:
            Exception : if removing handler fails
        """
        self.__other.handlers.remove(self)

class __log__(logging.Logger):

    def __init__(self, name: str = "NETWORK", level: int = logging.DEBUG):
        super().__init__(name, level)

        self.stream = StreamOutput(self)

        self.stream.enable()
        """
        Create a logger instance and attach a default `StreamOutput` handler.
        params:
            name : str : logger name
            level : int : logging level
        returns:
            None
        errors:
            Exception : if logger cannot be initialized
        """

    def format(self,record: CONNECTIONINFO):
        """
        Format a `CONNECTIONINFO` dataclass into a single-line log message.
        params:
            record : CONNECTIONINFO : connection summary object
        returns:
            str : formatted single-line summary
        errors:
            Exception : if formatting fails
        """
        return f"[{record.protocol}]:[{record.lname}] UUID={record.uuid}, STIME={record.stime}, ETIME={record.etime}, SRCADDR={record.srcaddr}, DSTADDR={record.dstaddr}, DATASENT={record.datas}, DATARECV={record.datar}, error={record.error}"