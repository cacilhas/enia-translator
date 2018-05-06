import os.path as path
from typing import Generator
from lxml import html
import requests
from . import stringdiff
from .settings import Settings, load_settings

class EniaWordSearcher:
    __slots__ = ('__tree', 'cachedir', 'min_score', 'url')

    def __init__(self, base_word: str, settings: Settings=None):
        settings = settings or load_settings()
        key = settings.translate.replace('-', '_')
        self.cachedir = settings.cachedir
        self.min_score = settings.min_score
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
        elements = self.tree.xpath(r'//*/text()')
        for element in (elements or ()):
            value = str(element).strip()
            if not value:
                continue

            score = stringdiff.score(word, value.split()[0],
                                     case_sensitive=False)
            if score >= self.min_score:
                yield value
