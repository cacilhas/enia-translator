import os.path as path
from typing import Generator
import string
from lxml import html
import requests
from .settings import Settings, load_settings


class EniaWordSearcher:
    __slots__ = ('__tree', 'cachedir', 'url')

    def __init__(self, base_word: str, settings: Settings=None):
        settings = settings or load_settings()
        key = settings.translate.replace('-', '_')
        self.cachedir = settings.cachedir
        self.url = getattr(settings.urls, key).format(
            word=base_word,
            lower=base_word.lower(),
            upper=base_word.upper(),
        )
        self.__tree = None

    @property
    def tree(self) -> html.HtmlElement:
        if not self.__tree:
            page_name = path.basename(self.url)
            page_file = path.join(self.cachedir, page_name)

            if path.exists(page_file):
                with open(page_file, 'rb') as fp:
                    content = fp.read()

            else:
                page = requests.get(self.url)
                page.raise_for_status()
                content = page.content
                with open(page_file, 'wb') as fp:
                    fp.write(content)

            self.__tree = html.fromstring(content)

        return self.__tree

    def search(self, word: str) -> Generator[str, None, None]:
        s = self.tree.xpath(
            '//*[starts-with('
            'translate(., "{ascii_lowercase}", "{ascii_uppercase}"),'
            '"{} "'
            ')]'
            .format(word.upper(), **string.__dict__)
        )
        for value in (s or ()):
            data = (value.text or '').strip()
            if data:
                yield data
