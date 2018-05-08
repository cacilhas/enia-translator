import asyncio
from asyncio import Future
from functools import partial
from typing import Callable
from .main import EniaWordSearcher
from .settings import Settings, load_settings

__all__ = ['search']

EventLoop = asyncio.AbstractEventLoop


def search(phrase: str, callback: Callable[[str], None], *,
           settings: Settings=None, loop: EventLoop=None) -> None:
    loop = loop or asyncio.get_event_loop()
    tasks = []
    for word in phrase.split():
        tasks.append(dispatch(word, settings, callback, loop=loop))
    loop.run_until_complete(
        asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, loop=loop)
    )


async def dispatch(word: str, settings: Settings,
                   callback: Callable[[str], None], loop: EventLoop) -> None:
    searcher = EniaWordSearcher(word, settings=settings)
    for result in searcher.search(word):
        callback(result)
        await asyncio.sleep(0, loop=loop)
