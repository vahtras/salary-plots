import os
import sys
import unittest.mock as mock

import pytest

from catplot.main import get_settings


@pytest.fixture
def sysargv():
    sys.argv[1:] = []
    return sys.argv


def test_data_from_env(sysargv):
    os.environ["data"] = "export.xlsx"
    settings = get_settings()
    assert settings["data"] == "export.xlsx"


def test_filters_from_env(sysargv):
    settings = get_settings()
    assert settings["filters"] == []

    os.environ['filters'] = "foo=bar baz=boo"
    settings = get_settings()
    assert settings["filters"] == ["foo=bar", "baz=boo"]


def test_data_from_cfg(sysargv):
    """
    Settings defined config.ini overrides environment variables

    $ export data=export.xlsx

    #config.ini
    [DEFAULT]
    data=alt.xlsx

    """
    os.environ["data"] = "export.xlsx"

    with mock.patch("catplot.main.ConfigParser") as mock_parser:
        mock_parser.return_value = mock.MagicMock()
        mock_config = mock_parser()
        mock_config.__getitem__.side_effect = lambda k: {
            "DEFAULT": {"data": "alt.xlsx"}
        }[k]

        settings = get_settings()

    mock_config.read.assert_called_with("config.ini")
    assert settings["data"] == "alt.xlsx"


def test_sub_category_from_plot_type_in_cfg(sysargv):
    """
    Verify subcategory in an ini.file

    [DEFAULT]
    foo=bar
    plot_type=point
    [point]
->  cat=dog

    """
    os.environ["data"] = "export.xlsx"
    with mock.patch("catplot.main.ConfigParser") as mock_parser:
        mock_parser.return_value = mock.MagicMock()
        mock_config = mock_parser()
        mock_config.__getitem__.side_effect = lambda k: {
            "DEFAULT": {"foo": "bar", "plot_type": "point"},
            "point": {"cat": "dog"},
        }[k]
        mock_config.sections.return_value = ["DEFAULT", "point"]
        settings = get_settings()

    mock_config.read.assert_called_with("config.ini")
    assert settings["cat"] == "dog"


def test_sub_category_from_plot_type_in_args(sysargv):
    """
    Command-line arguments overrides config.ini

    [DEFAULT]
    foo=bar
    [point]
    cat=dog


    $ catplot --plot-type point
    """

    with mock.patch("catplot.main.ConfigParser") as mock_parser:
        mock_parser.return_value = mock.MagicMock()
        mock_config = mock_parser()
        mock_config.__getitem__.side_effect = lambda k: {
            "DEFAULT": {"foo": "bar"},
            "point": {"cat": "dog"},
        }[k]
        mock_config.sections.return_value = ["DEFAULT", "point"]

        sysargv[1:] = '--plot-type point'.split()
        settings = get_settings(ini="config.ini")

    mock_config.read.assert_called_with("config.ini")
    assert settings["plot_type"] == "point"


def test_data_from_cmdline(sysargv):
    """
    Command-line data overrides environment variable

    catplot --data alt2.xlsx
    """
    os.environ["data"] = "export.xlsx"
    settings = get_settings()
    assert settings["data"] == "export.xlsx"

    sysargv[1:] = "--data alt2.xlsx".split()
    settings = get_settings(ini=None)
    assert settings["data"] == "alt2.xlsx"


def test_filters_from_cmdline_extends(sysargv):
    """
    Command-line data appends to environment variable

    $ env foo=bar catplot --filters baz=boo
    """
    settings = get_settings()
    assert settings['filters'] == []

    os.environ["filters"] = "foo=bar"
    settings = get_settings()
    assert settings["filters"] == ['foo=bar']

    sysargv[1:] = "--filters baz=boo".split()
    settings = get_settings()
    assert settings["filters"] == ['foo=bar', 'baz=boo']
