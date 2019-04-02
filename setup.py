#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'django-simplecms',
    version = '0.0.4',
    url = 'https://github.com/rtts/django-simplecms',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'django',
        'django-ckeditor',
        'django-embed-video',
        'easy-thumbnails',
    ],
)
