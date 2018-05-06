import os.path as path
from typing import Generator
from leven import levenshtein as leven
from lxml import html
import requests
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
        word = word.upper()
        elements = self.tree.xpath(r'//*/text()')
        for element in (elements or ()):
            value = str(element).strip()
            if not value:
                continue

            # TODO: function to calculate it
            ref = value.split()[0].upper()
            diff = leven(word, ref)
            if diff == 0:
                yield value
            else:
                length = max(len(word), len(ref))
                score = (length - diff) / length
                if score >= self.min_score:
                    yield value
