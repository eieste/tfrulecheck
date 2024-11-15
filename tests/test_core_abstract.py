# -*- coding: utf-8 -*-
import argparse

import pytest

from tfutility.core.abstract import AbstractCommand


def test_abstractcmd_constructor():
    x = AbstractCommand("a", "b")
    assert isinstance(x, AbstractCommand)
    assert x._cmd == "a"
    assert x.parser == "b"


def test_init():
    x = AbstractCommand("a", "b")
    with pytest.raises(NotImplementedError, match="Please Implement"):
        x._init()


def test_logger():
    class Sample:
        def get_logger(self):
            return "TEST"

    x = AbstractCommand(Sample(), "b")

    assert x.get_logger() == "TEST"


def test_add_arguments():
    x = AbstractCommand("a", "b")
    with pytest.raises(NotImplementedError, match=r"Please implement.*"):
        x.add_arguments(None)


def test_get_command_name():
    class NoneCommandName(AbstractCommand):
        command_name = None

    class DefinedCommandName(AbstractCommand):
        command_name = "commandname"

    x = NoneCommandName("a", "b")
    with pytest.raises(NotImplementedError, match=r"Please give your.*"):
        x.get_command_name()

    y = DefinedCommandName("a", "b")
    assert y.get_command_name() == "commandname"


def test_help():
    class NoneHelpText(AbstractCommand):
        help = "helptext"

    class DefinedHelpText(AbstractCommand):
        help = None

    x = DefinedHelpText("a", "b")
    with pytest.raises(NotImplementedError, match=r"Please give your.*"):
        x.get_help()

    y = NoneHelpText("a", "b")
    assert y.get_help() == "helptext"


def test_itsme():
    class TestClass(AbstractCommand):
        command_name = "commandfoo"
        help = "helptext"

    assert not TestClass(None, None).itsme(argparse.Namespace(command=None))
    assert not TestClass(None, None).itsme(argparse.Namespace(command="hiii"))

    assert TestClass(None, None).itsme(argparse.Namespace(command="commandfoo"))


def test_handle():
    class TestClass(AbstractCommand):
        command_name = "commandfoo"
        help = "helptext"

    with pytest.raises(NotImplementedError, match=r"Please implement this*"):
        assert not TestClass(None, None).handle(argparse.Namespace())
