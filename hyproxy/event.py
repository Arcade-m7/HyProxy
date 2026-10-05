from asyncio import gather, run

class Event:

    events = []

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
        run(
            cls.__ini__()
        )