#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as file:
    long_description = file.read()

setup(
    name = "Shinetech",
    version = "0.0.1",
    license = 'BSD',
    description = "Basic API for Shinetech IEMS",
    long_description=long_description,
    author='Bo Zhang',
    author_email='bozhang@shinetechchina.com',
    url='http://github.com/boer0327/xunlei',
    py_modules = ['shinetech'],
    install_requires = ['mechanize'],
    classifiers=[
        "Development Status :: 0.1 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Communications :: File Sharing",
    ],
)
