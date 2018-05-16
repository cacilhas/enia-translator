#!/usr/bin/env python3.6

from configparser import ConfigParser
import os.path as path
from setuptools import find_packages, setup

config = ConfigParser()
config.read(path.join(path.dirname(__file__), 'enia_translator', 'info.ini'))
main_conf = config['enia']
author_conf = config['author']
deps_conf = config['deps']

with open('./README.md') as fp:
    long_description = fp.read()

setup(
    name='enia-translator',
    version=main_conf['version'],
    provides=['enia_translator'],
    description=main_conf['description'],
    long_description=long_description,
    author=author_conf['name'],
    author_email=author_conf['contact'],
    url=config['repo']['url'],
    packages=find_packages(exclude=('tests', 'tests.*')),
    package_data={
        'enia_translator': ['info.ini'],
        'enia_translator._scripts': ['*.yaml'],
    },
    setup_requires=deps_conf['setup'].split(),
    install_requires=deps_conf['install'].split(),
    test_suite='tests',
    tests_require=deps_conf['test'].split(),
    entry_points={
        'console_scripts': [
            ' = '.join(pair) for pair in config['entry-points'].items()
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Framework :: AsyncIO',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
