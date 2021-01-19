import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sleepi",
    version="0.0.9",
    description="An async library for talking to SleepIQ",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/brianlich/sleepi",
    author="Brian Lich",
    author_email="blich29@hotmail.com",
    license="MIT license",
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
    packages=[find_packages(include=["sleepi"])],
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0"],
    keywords=["sleepiq", "sleep number", "async", "client"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)