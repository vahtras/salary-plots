import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt
import numpy as np
from catplot.plotters import BoxPlotter

Event = namedtuple("event", ["xdata", "ydata"])


@pytest.fixture
def df():
    # sample = 10
    # np.random.seed(0)
    # x = np.random.randint(20000, 40000, sample)
    # km = np.random.choice(['Kvinna', 'Man'], sample)
    # school = np.random.choice(['A', 'B', 'C'], sample)
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
        )
    )
    return _df[_df.kr > 0]


def test_box_setup(df):
    plotter = BoxPlotter(df, "kr", categorical="school")
    assert plotter.numerical == "kr"
    assert plotter.categorical == "school"


@pytest.fixture
def plx(df):
    return BoxPlotter(df, "kr")


def test_no_categorical_values(plx):
    assert plx.categorical_values() == []
    assert plx.hue_values() == []
    pdt.assert_series_equal(
        plx.set_y(),
        pd.Series([0.0] * 10, index=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10])
    )


def test_categorical_values(df):
    plotter = BoxPlotter(df, "kr", categorical="school")
    assert plotter.categorical_values() == ["A", "B", "C"]


@pytest.fixture
def plxy(df):
    return BoxPlotter(df, "kr", categorical="school")


@pytest.fixture
def plxyz(df):
    return BoxPlotter(df, "kr", categorical="school", hue="km")


@pytest.fixture
def plxzy(df):
    return BoxPlotter(df, "kr", categorical="km", hue="school")


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
    with mock.patch("catplot.plotters.sns.boxplot") as mockplot:
        plxyz.plot()
        mockplot.assert_called_once_with(
            data=plxyz.df,
            x="kr",
            y="school",
            hue="km",
            orient="h",
            whis=(10, 90),
            order=["A", "B", "C"],
            hue_order=["Kvinna", "Man"],
            showmeans=True,
            meanline=True,
            meanprops={'color': 'white'},
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
    plotter = BoxPlotter(
        df, "kr", categorical="school", hue="km", annotate=("Skola", "kr")
    )
    assert plotter.annotate == ("Skola", "kr")


def test_get_row_1(plx):
    row = plx.get_row(Event(30799, 0))
    pdt.assert_series_equal(row, plx.df.iloc[1])


def test_get_row_2(plxy):
    row = plxy.get_row(Event(35832, 0))
    pdt.assert_series_equal(row, plxy.df.iloc[9])


def test_get_row_2m(plxyz):
    row = plxyz.get_row(Event(35832, 0.2))
    pdt.assert_series_equal(row, plxyz.df.iloc[9])


def test_get_row_3(plxy):
    row = plxy.get_row(Event(22732, 1))
    pdt.assert_series_equal(row, plxy.df.iloc[0])


def test_get_row_4(plxy):
    row = plxy.get_row(Event(35430, 2))
    pdt.assert_series_equal(row, plxy.df.iloc[8])


def test_y_shift_2(plxyz):
    pdt.assert_series_equal(
        plxyz.y_shift(),
        pd.Series(
            [-0.2, -0.2, -0.2, 0.2, -0.2, 0.2, 0.2, -0.2, -0.2, 0.2],
            index=plxyz.df.index,
        ),
    )


def test_y_shift_3(plxzy):
    pdt.assert_series_equal(
        plxzy.y_shift(),
        pd.Series(
            [0, 0, 0, -0.8 / 3, 0, -0.8 / 3, -0.8 / 3, 0, 0.8 / 3, -0.8 / 3],
            index=plxzy.df.index,
        ),
    )


def test_no_hue(plxy):
    pdt.assert_series_equal(
        plxy.y_shift(), pd.Series(np.zeros(10), index=plxy.df.index)
    )
