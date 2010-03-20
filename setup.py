# YOU NEED TO EDIT THESE
AUTHOR = 'Chris Dent'
AUTHOR_EMAIL = 'python@example.org'
NAME = 'tiddlywebplugins.manifestopheles'
DESCRIPTION = 'A manifesto contextualizer'
VERSION = '0.1'


import os

from setuptools import setup, find_packages


# You should carefully review the below (install_requires especially).
setup(
    namespace_packages = ['tiddlywebplugins'],
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = 'http://pypi.python.org/pypi/%s' % NAME,
    packages = find_packages(exclude=['test']),
    platforms = 'Posix; MacOS X; Windows',
    install_requires = ['setuptools',
        'tiddlyweb',
        'tiddlywebplugins.utils',
        'tiddlywebplugins.templates',
        ],
    zip_safe = False
    )