#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'django-simplecms',
    version = '0.0.1',
    url = 'https://github.com/rtts/django-simplecms',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = ['cms'],
    install_requires = [
        'django',
        'django-ckeditor',
        'django-embed-video',
        'easy-thumbnails',
        'git+https://github.com/JaapJoris/django-simplecms.git',
    ],
)
