#!/bin/sh


pip install -e .
pip3 install -r requirements-dev.txt


exec $@
