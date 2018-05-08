from unittest import TestCase
from unittest.mock import patch
from collections import namedtuple
import os
import os.path as path
import shutil
from enia_translator import EniaWordSearcher
from enia_translator.settings import Settings
from . import vcr


class EniaWordSearcherTest(TestCase):
    maxDiff = None

    def setUp(self):
        temp_dir = path.realpath(path.join(
            path.dirname(__file__), path.pardir, 'tmp', 'enia',
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
        searcher = EniaWordSearcher('when', self.config)
        self.assertEqual(list(searcher.search('when')), ['WHEN quando'])

    @vcr.use_cassette('ceid-englishw.yaml')
    def test_search_for_otherw(self):
        searcher = EniaWordSearcher('when', self.config)
        self.assertEqual(list(searcher.search('web')),
                         ["WEB (spider's) tela (de aranea); (fig.) texito"])

    @vcr.use_cassette('ceid-englisha.yaml')
    def test_search_for_angel(self):
        searcher = EniaWordSearcher('angel', self.config)
        self.assertEqual(list(searcher.search('angel')), ['ANGEL angelo'])

    @vcr.use_cassette('ceid-englisha.yaml')
    def test_not_found(self):
        searcher = EniaWordSearcher('anima', self.config)
        self.assertEqual(list(searcher.search('anima')), [])

    def test_use_cache(self):
        with open(path.join(self.config.cachedir, 'ceid-englisha'), 'w') as fp:
            fp.write(
                '<html>'
                '<head></head>'
                '<body>'
                '<p>ALL omne</p>'
                '</body>'
                '</html>\n'
            )
        searcher = EniaWordSearcher('all', self.config)
        self.assertEqual(list(searcher.search('all')), ['ALL omne'])

    @vcr.use_cassette('ceid-englishw.yaml')
    def test_use_default_settings(self):
        with patch('enia_translator.main.load_settings',
                   return_value=self.config):
            searcher = EniaWordSearcher('when')
        self.assertEqual(list(searcher.search('when')), ['WHEN quando'])
