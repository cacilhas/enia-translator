#!/usr/bin/env python3.6

import os.path as path
from setuptools import find_packages, setup

setup(
    name='enia-translator',
    version='0.1',
    provides=['enia_translator'],
    description='Search for Interligua translations on-line',
    author='ℜodrigo Arĥimedeς ℳontegasppα ℭacilhας',
    author_email='batalema@cacilhas.info',
    url='https://bitbucket.org/cacilhas/enia-translator/src',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'lxml==4.2.1',
        'requests==2.18.4',
        'urllib3==1.22',
    ],
    test_suite='tests',
    tests_require=[
        'vcrpy==1.11.1',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
