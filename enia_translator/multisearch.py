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
        future = Future(loop=loop)
        future.add_done_callback(partial(pass_result, callback))
        tasks.append(dispatch(word, settings, future, loop))
    loop.run_until_complete(
        asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED, loop=loop)
    )


def pass_result(f: Callable[[str], None], future: Future) -> None:
    f(future.result())


async def dispatch(word: str, settings: Settings, future: Future,
                   loop: EventLoop) -> None:
    searcher = EniaWordSearcher(word, settings=settings)
    for result in searcher.search(word):
        future.set_result(result)
        await asyncio.sleep(0, loop=loop)
