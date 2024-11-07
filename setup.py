# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

f = open("VERSION", "r")
VERSION = f.read()
f.close()


f = open("README.md", "r")
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name="tfutility",
    version=VERSION,
    description="TfUtility provides different tools for Terraform Developers",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Stefan Eiermann",
    author_email="foss@ultraapp.de",
    url="https://github.com/eieste/tfutility.git",
    license="AGPLv3",
    packages=find_packages(),
    package_dir={"": "src"},
    package_data={"tfutility": ["templates/*"]},
    include_package_data=True,
    entry_points={"console_scripts": ["tfutility = tfutility.main:main"]},
)
