# -*- coding: utf-8 -*-
import logging
import re
import tempfile

import pytest

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


def test_forcedremotesource_local_source(mocker, caplog):
    INVALID_TF = """
        # @forcedremotesource
        module "test" {
            source = "../../foo"
        }
    """

    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(INVALID_TF.encode("utf-8"))
    tmpfile.close()

    mocker.patch("sys.argv", ["tfutility", "forcedremotesource", tmpfile.name])
    sysexit = mocker.patch("sys.exit")
    main()

    assert "Module Block has no" in caplog.text
    assert sysexit.call_args.args == (1,)
    assert sysexit.call_count == 1


def test_forcedremotesource_remotesource(mocker, caplog):
    VALID_TF = """
        # @forcedremotesource
        module "test" {
            source = "foo.com/test"
            version = "0.0.1"
        }
    """
    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(VALID_TF.encode("utf-8"))
    tmpfile.close()

    sysexit = mocker.patch("sys.exit")

    mocker.patch("sys.argv", ["tfutility", "forcedremotesource", tmpfile.name])
    sysexit = mocker.patch("sys.exit")
    main()

    assert "" in caplog.text
    assert sysexit.call_count == 0


def test_importdate_missing_decorator(mocker, caplog):
    MISSING_TF = """
        import {
            id = ""
            from = ""
        }
    """

    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(MISSING_TF.encode("utf-8"))
    tmpfile.close()

    mocker.patch("sys.argv", ["tfutility", "importdate", tmpfile.name])
    sysexit = mocker.patch("sys.exit")
    main()

    assert "Missing importdate Decorator above block" in caplog.text
    assert sysexit.call_args.args == (1,)
    assert sysexit.call_count == 1


def test_importdate_invaliddate(mocker, caplog):
    INVALID_DATE = """
        # @importdate(create="04-10-2019")
        import {
            id = ""
            from = ""
        }
    """
    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(INVALID_DATE.encode("utf-8"))
    tmpfile.close()

    mocker.patch(
        "sys.argv", ["tfutility", "importdate", "--expire-after", "10", tmpfile.name]
    )
    sysexit = mocker.patch("sys.exit")
    main()

    assert sysexit.call_args.args == (1,)
    assert "importdate Block expired " in caplog.text


def test_importdate_expirede(mocker, caplog):
    INVALID_DATE = """
        # @importdate(create="04-10-2019", expire="20-12-2019")
        import {
            id = ""
            from = ""
        }
    """
    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(INVALID_DATE.encode("utf-8"))
    tmpfile.close()

    mocker.patch("sys.argv", ["tfutility", "importdate", tmpfile.name])
    sysexit = mocker.patch("sys.exit")
    main()

    assert sysexit.call_args.args == (1,)
    assert "importdate Block expired " in caplog.text


def test_sourceswap_missing_parameters(mocker, caplog):
    INVALID_DATE = """
        # @sourceswap()
        module "hi" {
            source = ""
            version = ""
        }
    """
    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(INVALID_DATE.encode("utf-8"))
    tmpfile.close()

    mocker.patch(
        "sys.argv", ["tfutility", "sourceswap", tmpfile.name, "--switch-to", "local"]
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main()

    assert "requires the parameters" in caplog.text

    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_sourceswap_wrong_block(mocker, caplog):
    INVALID_DATE = """
        # @sourceswap(remotesource="..", remoteversion="0.0.1", localsource="..")
        resource "hi" "foo" {
            source = ".."
            version = "0.0.1"
        }
    """
    caplog.set_level(logging.INFO)

    tmpfile = tempfile.NamedTemporaryFile(suffix=".tf", delete_on_close=False)
    tmpfile.write(INVALID_DATE.encode("utf-8"))
    tmpfile.close()

    mocker.patch(
        "sys.argv", ["tfutility", "sourceswap", tmpfile.name, "--switch-to", "local"]
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main()

    assert "requires the parameters" in caplog.text

    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1
