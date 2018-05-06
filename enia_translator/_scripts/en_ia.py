from argparse import ArgumentParser
from enia_translator.multisearch import search
from enia_translator.settings import load_settings


def entrypoint() -> None:
    parser = ArgumentParser(description='translate en -> ia')
    parser.add_argument('words', type=str, nargs='+', help='word to search')
    args = parser.parse_args()
    search(' '.join(args.words), print)
