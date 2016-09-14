# -*- coding: utf-8 -*-
from setuptools import setup

from mutate import __version__, __author__


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='mutate',
    version=__version__,
    description='Python 2.7.x Mutation Testing',
    long_description=read("README.md"),
    author=__author__,
    author_email='',
    url='https://github.com/deefex/mutate',
    install_requires=open('requirements.txt').readlines(),
    license=read("LICENSE"),
    zip_safe=False,
    include_package_data=True,
    keywords='mutate',
    packages=['mutate', 'mutate.mutators'],
    entry_points={
        'console_scripts': [
            "mutate=mutate.mutate:main"
        ]
    },
)
