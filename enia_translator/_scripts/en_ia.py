from argparse import ArgumentParser
from enia_translator import EniaWordSearcher
from enia_translator.settings import load_settings


def entrypoint() -> None:
    parser = ArgumentParser(description='translate en -> ia')
    parser.add_argument('word', type=str, help='word to search')
    args = parser.parse_args()
    searcher = EniaWordSearcher(args.word, load_settings())
    for result in searcher.search(args.word):
        print(result)
