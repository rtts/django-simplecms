#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-simplecms',
    version = '1.0.3',
    url = 'https://github.com/rtts/django-simplecms',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['simplecms=cms.__main__:main'],
    },
    include_package_data = True,
    install_requires = [
        'django',
        'django-extensions',
        'django-embed-video',
        'easy-thumbnails',
        'libsass',
        'markdown',
        'psycopg2',
        'pylibmc',
    ],
)
