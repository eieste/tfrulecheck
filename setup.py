# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

f = open('VERSION', 'r')
VERSION = f.read()
f.close()



f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='tfutils',
    version=VERSION,
    description='TFUtils provides different tools for Terraform Developers',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Stefan Eiermann',
    author_email='foss@ultraapp.de',
    url='https://github.com/eieste/tfutils.git',
    license='AGPLv3',
    packages=find_packages(
        where='src',
        include=['tfutils*'],
    ),
    package_dir={"": "src"},
    package_data={'tfutils': ['templates/*']},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tfutils = tfutils.main:main"
        ]
    }
)
