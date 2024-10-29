from pathlib import Path
import sys
import unittest.mock as mock
from catplot.main import main

import pytest

@pytest.fixture
def cleanup():
    sys.argv[1:] = [
        "--data",
        "ftests/sample.csv",
        "--num",
        "Lon",
        "--cat",
        "Cat",
        "--title",
        "POSTDOKTOR",
        "--table",
        "0",
    ]
    yield
    Path('tab-Lon-Cat.csv').unlink()
    Path('tab-Lon-Cat.xlsx').unlink()

@mock.patch("catplot.main.plt.gcf")
@mock.patch("catplot.main.plt.show")
def test_boxplot(mock_show, mock_gcf, cleanup):
    with mock.patch("catplot.plotters.sns.boxplot") as mock_plot:
        sys.argv.extend(["--plot-type", "box"])
        main()
        assert mock_plot.called


@mock.patch("catplot.main.plt.gcf")
@mock.patch("catplot.main.plt.show")
def test_pointplot(mock_show, mock_gcf, cleanup):
    with mock.patch("catplot.plotters.sns.stripplot") as mock_plot:
        sys.argv.extend(["--plot-type", "point"])
        main()
        assert mock_plot.called
