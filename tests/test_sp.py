import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt
from catplot.plotters import StripPlotter

Event = namedtuple("event", ["xdata", "ydata"])


@pytest.fixture
def df():
    _df = pd.DataFrame(
        dict(
            kr=[
                22732,
                30799,
                29845,
                39648,
                33123,
                0,
                29225,
                34116,
                34935,
                35430,
                35832,
            ],
            km=[
                "Kvinna",
                "Kvinna",
                "Kvinna",
                "Man",
                "Kvinna",
                "Barn",
                "Man",
                "Man",
                "Kvinna",
                "Kvinna",
                "Man",
            ],
            school=["B", "B", "B", "A", "B", "D", "A", "A", "B", "C", "A"],
            age=[22, 23, 28, 21, 23, 1, 23, 23, 27, 20, 21],
        )
    )
    return _df[_df.kr > 0]


def test_strip_setup(df):
    plotter = StripPlotter(df, "kr", categorical="age")
    assert plotter.numerical == "kr"
    assert plotter.categorical == "age"


@pytest.fixture
def plx(df):
    return StripPlotter(df, "kr")


def test_no_categorical_values(plx):
    assert plx.categorical_values() == []
    assert plx.hue_values() == []
    pdt.assert_series_equal(
        plx.set_x(),
        pd.Series([0.0] * 10, index=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10])
    )


def test_categorical_values(df):
    plotter = StripPlotter(df, "kr", categorical="age")
    assert plotter.categorical_values() == ['20', '21', '22', '23', '27', '28']


def test_categorical_x_values(df):
    plotter = StripPlotter(df, "kr", categorical="age")
    assert all(plotter.set_x() == [2, 3, 5, 1, 3, 3, 3, 4, 0, 1])


@pytest.fixture
def plxy(df):
    return StripPlotter(df, "kr", categorical="age")


@pytest.fixture
def plxyz(df):
    return StripPlotter(df, "kr", categorical="age", hue="km")


@pytest.fixture
def plxzy(df):
    return StripPlotter(df, "kr", categorical="km", hue="school")


def test_hue_values(plxyz):
    assert plxyz.hue_values() == ["Kvinna", "Man"]


@mock.patch("catplot.plotters.plt.show")
def test_plot_subplots(mock_show, plxyz):
    with mock.patch("catplot.plotters.plt.subplots") as mockplots:
        mockplots.return_value = mock.Mock(), mock.Mock()
        plxyz.plot()
        mockplots.assert_called_once()


@mock.patch("catplot.plotters.plt.show")
def test_plot_seaborn(mock_show, plxyz):
    with mock.patch("catplot.plotters.sns.stripplot") as mockplot:
        plxyz.plot()
        mockplot.assert_called_once_with(
            data=plxyz.df,
            y="kr",
            x="age",
            hue="km",
            orient="v",
            order=['20', '21', '22', '23', '27', '28'],
            hue_order=["Kvinna", "Man"],
            jitter=0,
        )


@mock.patch("catplot.plotters.plt.show")
def test_hover_connect(mock_show, plxyz):
    with mock.patch("catplot.plotters.plt.subplots") as mock_plots:
        mock_fig = mock.MagicMock()
        mock_ax = mock.MagicMock()
        mock_plots.return_value = mock_fig, mock_ax
        plxyz.plot()
        mock_fig.canvas.mpl_connect.assert_called_with(
            "motion_notify_event", plxyz
        )


def test_annotate(df):
    plotter = StripPlotter(
        df, "kr", categorical="age", hue="km", annotate=("Skola", "kr")
    )
    assert plotter.annotate == ("Skola", "kr")


def test_get_row_1(plx):
    row = plx.get_row(Event(0, 35430))
    pdt.assert_series_equal(row, plx.df.iloc[8])


def test_get_row_2(plxy):
    row = plxy.get_row(Event(1, 35832))
    pdt.assert_series_equal(row, plxy.df.iloc[9])


def test_get_row_2m(plxyz):
    row = plxyz.get_row(Event(1, 35832))
    pdt.assert_series_equal(row, plxyz.df.iloc[9])


def test_get_row_3(plxy):
    row = plxy.get_row(Event(2, 22732))
    pdt.assert_series_equal(row, plxy.df.iloc[0])


def test_get_row_4(plxy):
    row = plxy.get_row(Event(0, 35430))
    pdt.assert_series_equal(row, plxy.df.iloc[8])
