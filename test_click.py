import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt
from click import *

Event = namedtuple('event', ['xdata', 'ydata'])

@pytest.fixture
def df():
    sample = 10
    #np.random.seed(0)
    #x = np.random.randint(20000, 40000, sample)
    #km = np.random.choice(['Kvinna', 'Man'], sample)
    #school = np.random.choice(['A', 'B', 'C'], sample)
    _df = pd.DataFrame(
        dict(
            kr=[22732, 30799, 29845, 39648, 33123,
               29225, 34116, 34935, 35430, 35832, 0],
            km=['Kvinna', 'Kvinna', 'Kvinna', 'Man', 'Kvinna',
                'Man', 'Man', 'Kvinna', 'Kvinna', 'Man', 'Man'],
            school=['B', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'C', 'A', 'A'],
        )
    )
    return _df[_df.kr > 0]
   
def test_setup(df):
    plotter = Plotter(df, "kr", "school")
    assert plotter.df is df
    assert plotter.x == "kr"
    assert plotter.category == "school"

@pytest.fixture
def plx(df):
    return Plotter(df, "kr")

def test_no_category_values(plx):
    assert plx.category_values() == []
    assert plx.hue_values() == []
    pdt.assert_series_equal(plx.set_y(), pd.Series(np.zeros(len(plx.df))))

def test_category_values(df):
    plotter = Plotter(df, "kr", "school")
    assert plotter.category_values() == ["A", "B", "C"]

@pytest.fixture
def plxy(df):
    return Plotter(df, "kr", "school")

@pytest.fixture
def plxyz(df):
    return Plotter(df, "kr", "school", "km")

@pytest.fixture
def plxzy(df):
    return Plotter(df, "kr", "km", "school")

def test_hue_values(plxyz):
    assert plxyz.hue_values() == ["Kvinna", "Man"]

@mock.patch('click.plt.show')
def test_boxplot_subplots(mock_show, plxyz):
    with mock.patch('click.plt.subplots') as mockplots:
        mockplots.return_value = mock.Mock(), mock.Mock()
        plxyz.boxplot()
        mockplots.assert_called_once()

@mock.patch('click.plt.show')
def test_boxplot_seaborn(mock_show, plxyz):
    with mock.patch('click.sns.boxplot') as mockplot:
        plxyz.boxplot()
        mockplot.assert_called_once_with(
            data=plxyz.df, x="kr", y="school", hue="km",
            whis=(10,90), order=["A", "B", "C"], 
            hue_order=["Kvinna", "Man"]
        )

def test_boxplot_show(plxyz):
    with mock.patch('click.plt.show') as mockshow:
        plxyz.boxplot()
        mockshow.assert_called_once()

def test_hover(df):
    hover = lambda: None
    plotter = Plotter(df, "kr", "school", "km", on_hover=hover)
    assert plotter.on_hover == hover

@mock.patch('click.plt.show')
def test_hover_connect(mock_show, plxyz):
    with mock.patch('click.plt.subplots') as mock_plots:
        mock_fig = mock.MagicMock()
        mock_ax = mock.MagicMock()
        mock_plots.return_value = mock_fig, mock_ax
        plxyz.boxplot()
        mock_fig.canvas.mpl_connect.assert_called_with('motion_notify_event', plxyz)

def test_annotate(df):
    plotter = Plotter(df, "kr", "school", "km", annotate=('Skola', 'kr'))
    assert plotter.annotate == ('Skola', 'kr')

def test_get_row_1(plx):
    row = plx.get_row(Event(30799, 0))
    pdt.assert_series_equal(row, plx.df.loc[1])

def test_get_row_2(plxy):
    row = plxy.get_row(Event(35832, 0))
    pdt.assert_series_equal(row, plxy.df.loc[9])

def test_get_row_2m(plxyz):
    row = plxyz.get_row(Event(35832, 0.2))
    pdt.assert_series_equal(row, plxyz.df.loc[9])

def test_get_row_3(plxy):
    row = plxy.get_row(Event(22732, 1))
    pdt.assert_series_equal(row, plxy.df.loc[0])

def test_get_row_4(plxy):
    row = plxy.get_row(Event(35430, 2))
    pdt.assert_series_equal(row, plxy.df.loc[8])

def test_y_shift_2(plxyz):
    pdt.assert_series_equal(plxyz.y_shift(), pd.Series([
        -.2, -.2, -.2, .2, -.2, 
        .2, .2, -.2, -.2, .2
        ])
    )

def test_y_shift_3(plxzy):
    pdt.assert_series_equal(plxzy.y_shift(), pd.Series([
        0, 0, 0, -.8/3, 0, 
        -.8/3, -.8/3, 0, .8/3, -.8/3
        ])
    )

def test_no_hue(plxy):
    pdt.assert_series_equal(plxy.y_shift(), pd.Series(np.zeros(10)))


