from ..policy import Policy
from ..utills import dns
from ..net import forwardfunction

from .log import __log__
from .auth import __auth__
from .sock import __connection__
from .cmd import __cmd__

from typing import Callable


class Config:
    
    def __init__(self):

        self.dns = dns
        self.privatemethod = None
        self.policy = Policy()

        self.log = __log__()
        self.cmd = __cmd__()
        self.auth = __auth__()
        self.connection = __connection__()
        self.call = forwardfunction

    def setprivatemethod(self, func: Callable):
        """
        params:
            func : Callable : callable to be used as private method handler
        returns:
            None
        errors:
            ValueError : if `func` is not callable
        """
        if callable(func):
            self.privatemethod = func
        else:
            raise ValueError(f'func must be callable')
        
    def setmitm(self,func: Callable):
        """
        params:
            func : Callable : callable to be used as MITM handler
        returns:
            None
        errors:
            ValueError : if `func` is not callable
        """
        if callable(func):
            self.mitm = func
        else:
            raise ValueError(f'{func} is not callable')