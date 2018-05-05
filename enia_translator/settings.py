import os
import os.path as path
from configparser import ConfigParser
from functools import lru_cache
from io import open
from numbers import Number
from typing import Any, Dict
from appdirs import user_config_dir

__all__ = ['Settings', 'load_settings']

Settings = Dict[str, Dict[str, Any]]


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    configdir = user_config_dir('enia-translator')
    if not path.exists(configdir):
        os.makedirs(configdir, exist_ok=True)

    cachedir = path.join(configdir, 'cache')
    if not path.exists(cachedir):
        os.makedirs(cachedir, exist_ok=True)

    config_filename = path.join(configdir, 'enia.ini')
    return {
        session.name: dict(session.items())
        for session in get_config(config_filename, cachedir).values()
    }


def get_config(fname: str, cachedir: str) -> ConfigParser:
    config = ConfigParser({'translate': 'en-ia'}, default_section='enia')
    config.add_section('local')
    config.add_section('web')
    config.set(
        'web', 'en-ia.url',
        'http://www.interlingua.com/an/ceid-english{lower[0]}',
    )
    config.set('local', 'cache', cachedir)

    if path.exists(fname):
        with open(fname) as fp:
            config.read_file(fp)

    with open(fname, 'w') as fp:
        config.write(fp)

    return config
