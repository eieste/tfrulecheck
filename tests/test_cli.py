# -*- coding: utf-8 -*-
import re

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
