"""Minimal setup file for tasks project."""

from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1.0',
    description='DrWeb task for position Puthon developer',

    author='Alexey Barannikov',
    author_email='alexwolf@inbox.ru',
    url='https://alexwolf.ru',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)