import sys, os
from setuptools import setup, find_packages
import subprocess

version = "0.3.0"

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
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.4"
    ],
    keywords="wayback machine archive",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    url="http://github.com/jsvine/waybackpack",
    license="MIT",
    version=version,
    packages=find_packages(exclude=["test",]),
    tests_require=[ "nose" ] + base_reqs,
    install_requires=base_reqs,
    entry_points={
        "console_scripts": [ "waybackpack = waybackpack.cli:main" ]
    }
)
