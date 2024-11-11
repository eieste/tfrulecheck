# -*- coding: utf-8 -*-
import argparse
import logging
import pathlib
import tempfile

import pytest

from tfutility.core.exp import PathIsNotValid
from tfutility.core.tfpaths import TfPaths


def test_get_file_list_invalid_path(caplog):
    parser = argparse.ArgumentParser()

    class Foo:
        def get_logger(self):
            log = logging.getLogger()
            return log

    test = TfPaths(Foo(), parser)
    with pytest.raises(PathIsNotValid, match="Path does not exist"):
        test.get_file_list(
            [
                pathlib.Path("hjklvskjhsdfhkjgsd/"),
            ]
        )

    with tempfile.NamedTemporaryFile(suffix=".tf") as tfile:
        test.get_file_list(
            [
                pathlib.Path(tfile.name),
            ]
        )

    with tempfile.TemporaryDirectory() as tdir:
        test.get_file_list(
            [
                pathlib.Path(tdir),
            ]
        )
        assert "found Zero files" in caplog.text


def test_add_arguments():
    parser = argparse.ArgumentParser()

    class Foo:
        def get_logger(self):
            log = logging.getLogger()
            return log

    TfPaths(Foo(), parser)
