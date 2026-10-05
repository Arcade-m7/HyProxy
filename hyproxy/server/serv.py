from ..event import Event
from .asynclistner import Asynclistener

from typing import Awaitable

async def contoller(s):
    pass

class Server(Event):

    def __init__(self, *Listeners: list[Asynclistener], Contoller: Awaitable = contoller):
        """
        Store provided `Asynclistener` instances for orchestration.
        params:
            *Listeners : list[Asynclistener] : Asynclistener instances to manage
        returns:
            None
        errors:
            Exception : if invalid listeners provided
        """
        self.Listeners = Listeners
        for listener in Listeners:
            self.addevent(
                listener.serv()
            )

        self.addevent(
            Contoller(self)
        )