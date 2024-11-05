# -*- coding: utf-8 -*-
import argparse
import logging
import pathlib
import tempfile

import pytest

from tfutils.core.exp import PathIsNotValid
from tfutils.core.tfpaths import TFPaths


def test_get_file_list_invalid_path(caplog):
    parser = argparse.ArgumentParser()

    class Foo:

        def get_logger(self):
            log = logging.getLogger()
            return log

    test = TFPaths(Foo(), parser)
    with pytest.raises(PathIsNotValid, match='Path does not exist' ):
        a = test.get_file_list([
            pathlib.Path("hjklvskjhsdfhkjgsd/"),
        ])

    with tempfile.NamedTemporaryFile(suffix=".tf") as tfile:
        a = test.get_file_list([
            pathlib.Path(tfile.name),
        ])

    with tempfile.TemporaryDirectory() as tdir:
        a = test.get_file_list([
            pathlib.Path(tdir),
        ])
        assert "found Zero files" in caplog.text


def test_add_arguments():
    parser = argparse.ArgumentParser()

    class Foo:

        def get_logger(self):
            log = logging.getLogger()
            return log

    test = TFPaths(Foo(), parser)
