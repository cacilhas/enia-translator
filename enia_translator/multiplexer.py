import asyncio
from functools import partial
from typing import Any, Callable, Iterable, TypeVar

__all__ = ['distribute']

T1 = TypeVar('T1')
T2 = TypeVar('T2')


def distribute(f: Callable[[T1], T2],
               args: Iterable[T1],
               callback: Callable[[T2], None], *,
               loop: asyncio.AbstractEventLoop=None) -> None:
    loop = loop or asyncio.get_event_loop()
    tasks = []
    for arg in args:
        future = asyncio.Future(loop=loop)
        future.add_done_callback(partial(call_result, callback))
        tasks.append(coro(partial(f, arg), future))
    loop.run_until_complete(asyncio.gather(*tasks, loop=loop))


def call_result(f: Callable[[Any], None], future: asyncio.Future) -> None:
    f(future.result())


async def coro(f: Callable[[], None], future: asyncio.Future) -> None:
    future.set_result(f())
