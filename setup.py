import sys, os
from setuptools import setup, find_packages
import subprocess

version = {}
with open("waybackpack/version.py") as fp:
    exec(fp.read(), version)

base_reqs = [
    "requests"
]

setup(
    name="waybackpack",
    description="Command-line tool that lets you download the entire Wayback Machine archive for a given URL.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="wayback machine archive",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    url="https://github.com/jsvine/waybackpack",
    license="MIT",
    version=version["__version__"],
    packages=find_packages(exclude=["test",]),
    tests_require=[ "pytest", "pytest-coverage" ] + base_reqs,
    extras_require = {
        'full': ['tqdm']
    },
    install_requires=base_reqs,
    entry_points={
        "console_scripts": [ "waybackpack = waybackpack.cli:main" ]
    }
)
