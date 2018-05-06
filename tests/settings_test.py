from unittest import TestCase
from unittest.mock import call, patch
import os
import os.path as path
from io import StringIO
from enia_translator.settings import Settings, load_settings


class LoadSettingsTest(TestCase):
    maxDiff = None

    def setUp(self):
        temp_dir = path.join(path.realpath(os.curdir), 'tmp', 'enia')
        self.user_config_dir = patch('enia_translator.settings.user_config_dir')
        ucd = self.user_config_dir.start()
        self.temp_dir = ucd.return_value = temp_dir

    def tearDown(self):
        self.user_config_dir.stop()
        load_settings.cache_clear()

    @patch('enia_translator.settings.open')
    @patch('enia_translator.settings.path.exists')
    def test_create_config_file(self, exists, open_mock):
        with StringIO() as iop:
            buf = IOWrapper(wrapped=iop)

            def side_effect(filename, mode='r') -> StringIO:
                return buf

            exists.return_value = False
            open_mock.side_effect = side_effect
            config = load_settings()

            fname = path.join(self.temp_dir, 'enia.ini')
            cachedir = path.join(self.temp_dir, 'cache')
            self.assertIn(call(fname), exists.call_args_list)
            exists.assert_called_with(fname)
            open_mock.assert_called_once_with(fname, 'w')
            self.assertEqual(config, Settings(
                cachedir=cachedir,
                translate='en-ia',
                min_score=.75,
                urls=config.urls_class(
                    en_ia='http://www.interlingua.com/an/'
                          'ceid-english{lower[0]}',
                ),
                urls_class=config.urls_class,
            ))
            self.assertTrue(buf.closed)
            self.assertEqual(iop.getvalue(),
                '[enia]\n'
                'translate = en-ia\n'
                'min-score = 0.75\n\n'
                '[local]\n'
                'cache = {cachedir}\n\n'
                '[web]\n'
                'en-ia.url = '
                'http://www.interlingua.com/an/ceid-english{{lower[0]}}\n\n'
                .format(cachedir=cachedir)
            )

    @patch('enia_translator.settings.open')
    @patch('enia_translator.settings.path.exists')
    def test_reuse_config(self, exists, open_mock):
        def side_effect(filename, mode='r') -> StringIO:
            return StringIO()

        exists.return_value = False
        open_mock.side_effect = side_effect
        config = load_settings()
        self.assertIs(config, load_settings())

    @patch('enia_translator.settings.open')
    @patch('enia_translator.settings.path.exists')
    def test_use_existent_config_file(self, exists, open_mock):
        with StringIO() as iop:
            buf = IOWrapper(wrapped=iop)

            def side_effect(filename, mode='r') -> StringIO:
                return buf if mode == 'w' else StringIO(
                    '[enia]\n'
                    'translate = ia-en\n'
                    'min-score = 0.8\n'
                    '[local]\n'
                    'cache = /tmp\n\n'
                    '[web]\n'
                    'ia-en.url = '
                    'http://www.google.com/search?q={word}\n'
                )

            exists.return_value = True
            open_mock.side_effect = side_effect
            config = load_settings()

            fname = path.join(self.temp_dir, 'enia.ini')
            self.assertIn(call(fname), exists.call_args_list)
            exists.assert_called_with(fname)
            self.assertEqual(open_mock.call_args_list, [
                call(fname),
                call(fname, 'w'),
            ])
            self.assertEqual(config, Settings(
                cachedir='/tmp',
                translate='ia-en',
                min_score=.8,
                urls=config.urls_class(
                    en_ia='http://www.interlingua.com/an/'
                          'ceid-english{lower[0]}',
                    ia_en='http://www.google.com/search?q={word}',
                ),
                urls_class=config.urls_class,
            ))
            self.assertTrue(buf.closed)
            self.assertEqual(iop.getvalue(),
                '[enia]\n'
                'translate = ia-en\n'
                'min-score = 0.8\n\n'
                '[local]\n'
                'cache = /tmp\n\n'
                '[web]\n'
                'en-ia.url = '
                'http://www.interlingua.com/an/ceid-english{lower[0]}\n'
                'ia-en.url = '
                'http://www.google.com/search?q={word}\n\n'
            )

    @patch('enia_translator.settings.open')
    @patch('enia_translator.settings.path.exists')
    def test_use_partial_config_file(self, exists, open_mock):
        with StringIO() as iop:
            buf = IOWrapper(wrapped=iop)

            def side_effect(filename, mode='r') -> StringIO:
                return buf if mode == 'w' else StringIO(
                    '[enia]\n'
                    'min-score = 0.9\n\n'
                    '[local]\n'
                    'cache = /tmp\n'
                )

            exists.return_value = True
            open_mock.side_effect = side_effect
            config = load_settings()

            fname = path.join(self.temp_dir, 'enia.ini')
            self.assertIn(call(fname), exists.call_args_list)
            exists.assert_called_with(fname)
            self.assertEqual(open_mock.call_args_list, [
                call(fname),
                call(fname, 'w'),
            ])
            self.assertEqual(config, Settings(
                cachedir='/tmp',
                translate='en-ia',
                min_score=.9,
                urls=config.urls_class(
                    en_ia='http://www.interlingua.com/an/'
                          'ceid-english{lower[0]}',
                ),
                urls_class=config.urls_class,
            ))
            self.assertTrue(buf.closed)
            self.assertEqual(iop.getvalue(),
                '[enia]\n'
                'translate = en-ia\n'
                'min-score = 0.9\n\n'
                '[local]\n'
                'cache = /tmp\n\n'
                '[web]\n'
                'en-ia.url = '
                'http://www.interlingua.com/an/ceid-english{lower[0]}\n\n'
            )


class IOWrapper(StringIO):

    def __init__(self, *args, wrapped: StringIO, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapped = wrapped

    def close(self) -> None:
        self.wrapped.write(self.getvalue())
        return super().close()
