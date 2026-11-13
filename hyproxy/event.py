from asyncio import gather, run

class Event:

    events = []
    isrunning = None

    @classmethod
    async def __ini__(cls):
        return await gather(
            *cls.events
        )

    @classmethod
    def addevent(cls, event):
        cls.events.append(event)

    @classmethod
    def popevent(cls, index: int):
        cls.events.pop(index)

    @classmethod
    def run(cls):
        cls.isrunning = True
        run(
            cls.__ini__()
        )

    @classmethod
    def stop(cls):
        cls.isrunning = False
        pass