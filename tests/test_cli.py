# -*- coding: utf-8 -*-
import logging
import re
import tempfile

from tfutility.main import main

VESION_REGEX = re.compile(r"^(\d+\.)?(\d+\.)?(\*|\d+)$")


def test_empty(capsys, mocker):
    mocker.patch("sys.argv", ["tfutility"])
    tfdo = mocker.patch("tfutility.main.TfUtility.do")
    main()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert tfdo.call_count == 1


def test_version(capsys, mocker):
    mocker.patch("sys.argv", ["tfutility", "-V"])
    sysexit = mocker.patch("sys.exit")
    main()
    captured = capsys.readouterr()
    assert VESION_REGEX.match(captured.out) is not None
    assert sysexit.call_count == 1


def test_forcedremotesource(mocker, caplog):
    INVALID_TF = """
        # @forcedremotesource
        module "test" {
            source = "../../foo"
        }
    """

    VALID_TF = """
        # @forcedremotesource
        module "test" {
            source = "foo.com/test"
            version = "0.0.1"
        }
    """
    caplog.set_level(logging.INFO)

    valid_temp = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    valid_temp.write(VALID_TF.encode("utf-8"))
    valid_temp.close()

    invalid_temp = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    invalid_temp.write(INVALID_TF.encode("utf-8"))
    invalid_temp.close()

    # "tfutility",
    mocker.patch("sys.argv", ["tfutility", "forcedremotesource", invalid_temp.name])
    sysexit = mocker.patch("sys.exit")
    main()

    assert "Module Block has no" in caplog.text
    assert sysexit.call_args.args == (1,)
    assert sysexit.call_count == 1
