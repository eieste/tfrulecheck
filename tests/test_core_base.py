# -*- coding: utf-8 -*-
import argparse
import pathlib
import sys
import tempfile

import pytest

from tfutility.core.base import Command
from tfutility.core.tffile import TfFile
from tfutility.core.tfpaths import TfPaths
from tfutility.main import main


class FooBar(TfPaths, Command):
    command_name = "foobardecorator"
    help = "Check if a RemoteSource was set"

    def new_decorator(self, options, block):
        file_path = block.tffile.path
        if not block.id.startswith("foobarblock"):
            self.get_logger().error(
                "The decorator @foobarblock can only applied to modules"
            )
            sys.exit(1)

        block_content = block.content

        if not block_content.get("mustexist"):
            self._error = True
            self.get_logger().error(
                "foobar Block had no mustexist Defined in {}:{}".format(
                    file_path, block.start
                )
            )

    def handle(self, options):
        self._error = False

        tf_files = self.get_file_list(options.paths)

        for file in tf_files:
            file = TfFile(file)
            for block in file.get_blocks_with_decorator(self.get_command_name()):
                self.new_decorator(self, block)


def test_base_tfpaths_required(mocker):
    mocker.patch("sys.argv", ["tfutility", "foobardecorator"])
    mocker.patch("tfutility.main.TfUtility.handlers", [FooBar])

    def error(self, message):
        raise ValueError(message)

    mocker.patch("argparse.ArgumentParser.error", error)

    with pytest.raises(ValueError, match=r".*required: paths"):
        main()


def test_tfpath_parsing(mocker):
    mocker.patch("tfutility.main.TfUtility.handlers", [FooBar])
    VALID_TF = """
        # @foobardecorator
        foobarblock "test" {
            source = "foo.com/test"
            version = "0.0.1"
        }
    """
    valid_temp = tempfile.NamedTemporaryFile(suffix=".tf")
    valid_temp.write(VALID_TF.encode("utf-8"))
    valid_temp.seek(0)
    mocker.patch("sys.argv", ["tfutility", "foobardecorator", valid_temp.name])

    foobar_obj = FooBar(None, None)

    assert foobar_obj.get_command_name() == foobar_obj.command_name
    assert foobar_obj.command_name == "foobardecorator"
    assert foobar_obj.itsme(argparse.Namespace(command="hallo")) is False
    assert foobar_obj.itsme(argparse.Namespace(command="foobardecorator"))

    tmpath = pathlib.Path(valid_temp.name)
    assert all(
        [p.as_posix() == valid_temp.name for p in foobar_obj.get_file_list([tmpath])]
    )

    new_dec = mocker.patch.object(foobar_obj, "new_decorator")

    main()

    foobar_obj.handle(
        argparse.Namespace(
            command="foobardecorator", paths=[pathlib.Path(valid_temp.name)]
        )
    )
    assert new_dec.call_count == 1


def test_cmd_handle(mocker):
    VALID_TF = """
        # @foobardecorator
        foobarblock "test" {
            source = "foo.com/test"
            version = "0.0.1"
        }
    """

    valid_temp = tempfile.NamedTemporaryFile(suffix=".tf")
    valid_temp.write(VALID_TF.encode("utf-8"))
    testoptions = argparse.Namespace(
        command="foobardecorator", paths=[pathlib.Path(valid_temp.name)]
    )

    foobar_obj = FooBar(None, None)

    tmpath = pathlib.Path(valid_temp.name)

    filelist = mocker.patch.object(foobar_obj, "get_file_list", return_value=[tmpath])
    getblock = mocker.patch("tfutility.core.tffile.TfFile.get_blocks_with_decorator")
    new_dec = mocker.patch.object(foobar_obj, "new_decorator")

    foobar_obj.handle(testoptions)

    assert getblock.call_count == 1
    assert filelist.call_count == 1
    assert new_dec.call_count == 0
