# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='slack-pinned-storage',
    version='0.0.1',
    description='A super progressive storage interface',
    long_description=readme,
    license=license,
    author='RyoNkmr',
    author_email='ryonakamuraryo@gmail.com',
    url='https://github.com/room8.fm/slack-pinned-storage',
    install_requires=['requests', 'python-dateutil'],
    packages=find_packages(exclude=('tests', 'docs'))
)
