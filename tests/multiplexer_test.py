from unittest import TestCase
from unittest.mock import patch
import asyncio
from enia_translator.multiplexer import distribute


class DistributeTest(TestCase):

    def test_collect_data(self):
        func = lambda x: x * 2
        buf = set()
        callback = lambda x: buf.add(x)
        distribute(func, range(10), callback)
        self.assertEqual(buf, set(range(0, 20, 2)))

    def test_use_supplied_loop(self):
        loop = asyncio.new_event_loop()
        func = lambda x: x + 1
        buf = set()
        callback = lambda x: buf.add(x)
        with patch('asyncio.get_event_loop', side_effect=AssertionError):
            distribute(func, range(10), callback, loop=loop)
        self.assertEqual(buf, set(range(1, 11)))
