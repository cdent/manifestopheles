# YOU NEED TO EDIT THESE
AUTHOR = 'Chris Dent'
AUTHOR_EMAIL = 'python@example.org'
NAME = 'tiddlywebplugins.manifestopheles'
DESCRIPTION = 'A manifesto contextualizer'
VERSION = '0.3'


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
    scripts = ['hell'],
    url = 'http://pypi.python.org/pypi/%s' % NAME,
    packages = find_packages(exclude=['test']),
    platforms = 'Posix; MacOS X; Windows',
    install_requires = ['setuptools',
        'tiddlyweb>=1.4.0',
        'tiddlywebplugins.utils',
        'tiddlywebplugins.templates',
        'tiddlywebplugins.imaker',
        ],
    zip_safe = False,
    include_package_data = True,
    )
