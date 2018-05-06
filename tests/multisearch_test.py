from unittest import TestCase
import asyncio
from collections import namedtuple
from functools import partial
import os
import os.path as path
import shutil
from . import vcr
from enia_translator.multisearch import search
from enia_translator.settings import Settings


class MultisearchTest(TestCase):
    maxDiff = None

    def setUp(self):
        temp_dir = path.realpath(path.join(
            path.dirname(__file__), '..', 'tmp', 'enia',
        ))
        urls_class = namedtuple('URLs', 'en_ia')
        self.config = Settings(
            cachedir=path.join(temp_dir, 'cache'),
            translate='en-ia',
            min_score=.95,
            urls=urls_class(
                en_ia='http://www.interlingua.com/an/ceid-english{lower[0]}',
            ),
            urls_class=urls_class,
        )
        os.makedirs(self.config.cachedir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.config.cachedir)

    @vcr.use_cassette('ceid-englishw.yaml')
    def test_search_for_when(self):
        buf = set()
        search('when what who', partial(buf.add), settings=self.config)
        self.assertEqual(buf, {
            'WHAT adj qual, que; interj como!; pron que; (that which) lo que',
            'WHEN quando',
            'WHO pron (interrogative) qui; (relative) qui, le qual(es)',
        })

    @vcr.use_cassette('ceid-englisha.yaml')
    def test_use_supplied_loop(self):
        loop = asyncio.new_event_loop()
        try:
            buf = set()
            search('all away aside', partial(buf.add), settings=self.config,
                loop=loop)
            self.assertEqual(buf, {
                'ALL adj omne, tote; adv completemente; (everybody) omnes,'
                ' totes; (everything) \n    toto; (at - ) del toto',
                'ASIDE adj parte, al latere',
                'AWAY foras, via; XXX-KILOMETRES- a xxx kilometros',
            })
        finally:
            loop.close()
