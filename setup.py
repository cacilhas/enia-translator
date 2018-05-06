#!/usr/bin/env python3.6

import os.path as path
from setuptools import find_packages, setup

with open('./README.md') as fp:
    long_description = fp.read()

setup(
    name='enia-translator',
    version='1.2.0',
    provides=['enia_translator'],
    description='Search for Interligua translations on-line',
    long_description=long_description,
    author='ℜodrigo ℭacilhας',
    author_email='batalema@cacilhas.info',
    url='https://bitbucket.org/cacilhas/enia-translator/',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'appdirs==1.4.3',
        'leven==1.0.4',
        'lxml==4.2.1',
        'requests==2.18.4',
        'urllib3==1.22',
    ],
    test_suite='tests',
    tests_require=[
        'vcrpy==1.11.1',
    ],
    entry_points={
        'console_scripts': [
            'en-ia = enia_translator._scripts.en_ia:entrypoint',
            'x-en-ia = enia_translator._scripts.gui:entrypoint',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
