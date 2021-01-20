from os import read, system
import os
import pathlib
import re
import sys
from setuptools import setup, find_packages

def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("sleepi", "__version__.py")
    return re.search(regex, read(*path)).group("version")

def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()

with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    author="Brian Lich",
    author_email="blich29@hotmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="An async library for SleepIQ (Sleep Number)",
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0"],
    keywords=["sleepiq", "sleep number", "async", "client"],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="sleepi",
    packages=find_packages(include=["sleepi"]),
    url="https://github.com/brianlich/sleepi",
    version=get_version(),
    zip_safe=False,
)