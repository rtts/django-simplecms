#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'django-simplecms',
    description = 'Simple Django CMS',
    version = '1.0.3',
    author = 'Jaap Joris Vens',
    author_email = 'jj+cms@rtts.eu',
    url = 'https://github.com/rtts/django-simplecms',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['simplecms=cms.__main__:main'],
    },
    include_package_data = True,
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.8',
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
