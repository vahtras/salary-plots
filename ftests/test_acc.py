import sys
import unittest.mock as mock
from catplot.main import main


@mock.patch("catplot.main.plt.show")
def test_boxplot(mock_show):
    sys.argv[1:] = [
        "--data",
        "ftests/sample.csv",
        "--num",
        "Lon",
        "--cat",
        "Cat",
        "--plot-type",
        "box",
        "--title",
        "POSTDOKTOR",
        "--table",
        "0",
    ]
    with mock.patch("catplot.plotters.sns.boxplot") as mock_plot:
        main()
        assert mock_plot.called


@mock.patch("catplot.main.plt.show")
def test_pointplot(mock_show):
    sys.argv[1:] = [
        "--data",
        "ftests/sample.csv",
        "--num",
        "Lon",
        "--cat",
        "Cat",
        "--plot-type",
        "point",
        "--title",
        "POSTDOKTOR",
        "--table",
        "0",
    ]
    with mock.patch("catplot.plotters.sns.stripplot") as mock_plot:
        main()
        assert mock_plot.called
