# -*- coding utf-8 -*-
# !/usr/bin/env python

# setuptools imports
from setuptools import setup
from setuptools import find_packages

# pybooru imports
import pybooru


# Read description file
with open('README.md', 'r') as f:
    long_description = f.read()

extras = {
    'tests': ['unittest2']
}

setup(
    name="Pybooru",
    version=pybooru.__version__,
    author=pybooru.__author__,
    description="Pybooru is a Python package to access to the API of Danbooru/Moebooru based sites.",
    long_description=long_description,
    author_email="danielluque14@gmail.com",
    url="https://github.com/LuqueDaniel/pybooru",
    license="MIT License",
    keywords="Pybooru moebooru danbooru API client",
    packages=find_packages(),
    platforms=['any'],
    install_requires=['requests'],
    extras_require=extras,
    include_package_data=True,
    data_file=[
        ('', ['LICENSE', 'README.md', 'changelog.md', 'requirements.txt'])
        ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet"
        ],
    entry_points={
        "console_scripts": [
            "tests = pybooru.tests.testing:main [tests]",
        ],
    }
)
