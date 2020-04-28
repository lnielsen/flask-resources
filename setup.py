# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs"""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "check-manifest>=0.25",
    "coverage>=4.0",
    "isort>=4.3.3",
    "pydocstyle>=2.0.0",
    "pytest-cov>=2.5.1",
    "pytest-pep8>=1.0.6",
    "pytest-invenio>=1.2.1",
    "invenio-app",  # TODO pin version
    "redis",  # TODO is it needed? for now only for app fixture
    "invenio-db[postgresql]",  # TODO move depency somewhere more maintanable
    "invenio-search[elasticsearch7]",  # TODO move depency somewhere more maintanable
]

extras_require = {
    "docs": ["Sphinx>=1.5.1",],
    "tests": tests_require,
}

extras_require["all"] = []
for reqs in extras_require.values():
    extras_require["all"].extend(reqs)

setup_requires = [
    "Babel>=1.3",
    "pytest-runner>=3.0.0,<5",
]

install_requires = [
    # TODO pin versions
    "Flask-BabelEx>=0.9.4",
    "invenio-base",
    "invenio-db",
    "invenio-pidstore",
    "invenio-search",
    "invenio-indexer",
    "invenio-records",
    # FIXME: add when released
    # "flask-resources",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("invenio_resources", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="invenio-resources",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio TODO",
    license="MIT",
    author="CERN",
    author_email="info@inveniosoftware.org",
    url="https://github.com/inveniosoftware/invenio-resources",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_base.apps": [
            "invenio_resources = invenio_resources:InvenioResources",
        ],
        "invenio_i18n.translations": ["messages = invenio_resources",],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
    ],
)
