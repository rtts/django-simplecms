#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-simplecms',
    version = '2.1.0',
    url = 'https://github.com/rtts/django-simplecms',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = find_packages(),
    scripts = ['bin/simplecms'],
    include_package_data = True,
    install_requires = [
        'django',
        'django-ckeditor',
        'django-extensions',
        'django-embed-video',
        'django-polymorphic',
        'easy-thumbnails',
        'psycopg2',
        'libsass',
        'swapper',
    ],
)
