from unittest import mock
from collections import namedtuple

import pytest

from catplot import main, plotters

Event = namedtuple("event", ["xdata", "ydata"])


@pytest.mark.parametrize(
    'numerical, categorical',
    [
        ('Salary', 'Gender'),
        ('Lön', 'Kön'),
    ]
)
def test_pp_default_setup(numerical, categorical, df):
    plotter = plotters.PointPlotter(df, numerical, categorical=categorical)
    assert plotter.df is df
    assert plotter.numerical == numerical
    assert plotter.categorical == categorical


def test_pp_plot(df):
    # df_sorted = pd.read_csv('test_pp_plot.csv')
    pp = plotters.PointPlotter(df, numerical="kr", categorical="km")

    with mock.patch("catplot.plotters.sns.stripplot") as mock_stripplot:
        pp.plot()

    mock_stripplot.assert_called()


def test_read_csv_data():
    with mock.patch("catplot.main.pd.read_csv") as mock_csv:
        main.process_data("exported.csv")
        mock_csv.assert_called


def test_read_xl_data():
    with mock.patch("catplot.main.pd.read_excel") as mock_xl:
        main.process_data("exported.xlsx")
        mock_xl.assert_called
