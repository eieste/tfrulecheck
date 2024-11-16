#!/bin/sh


pip install -e '.[dev]'
pip install -e .


exec $@
