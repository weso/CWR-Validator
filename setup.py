# -*- coding: utf-8 -*-
import ast
import re
from codecs import open
from os import path

from setuptools import find_packages, setup

__license__ = "MIT"

_version_re = re.compile(r"__version__\s+=\s+(.*)")
_tests_require = ["pytest"]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("cwr_validator/__init__.py", "rb", encoding="utf-8") as f:
    version = f.read()
    version = _version_re.search(version).group(1)
    version = str(ast.literal_eval(version.rstrip()))

setup(
    name="CWR-Validator",
    packages=find_packages(),
    include_package_data=True,
    version=version,
    description="CLI validator for CWR v2.1 and v2.2 files using local DataApi libraries",
    author="WESO",
    author_email="weso@weso.es",
    license="MIT",
    url="https://github.com/max1millions/CWR-Validator",
    keywords=["CWR", "commonworks", "validator", "CISAC"],
    platforms="any",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pyparsing>=3.0.0,<3.1.0",
        "pyyaml>=3.11",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "validate-cwr=cwr_validator.cli:main",
        ],
    },
    tests_require=_tests_require,
    extras_require={"test": _tests_require},
)
