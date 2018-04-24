import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.util.testing as pdt
from click import *

@pytest.fixture
def df():
    sample = 10
    #np.random.seed(0)
    #x = np.random.randint(20000, 40000, sample)
    #km = np.random.choice(['Kvinna', 'Man'], sample)
    #school = np.random.choice(['A', 'B', 'C'], sample)
    return pd.DataFrame(
        dict(
            x=[22732, 30799, 29845, 39648, 33123,
               29225, 34116, 34935, 35430, 35832],
            km=['Kvinna', 'Kvinna', 'Kvinna', 'Man', 'Kvinna',
                'Man', 'Man', 'Kvinna', 'Kvinna', 'Man'],
            school=['B', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'C', 'A'],
        )
    )
   
def test_setup(df):
    plotter = Plotter(df, "x", "school")
    assert plotter.df is df
    assert plotter.x == "x"
    assert plotter.category == "school"

def test_category_values(df):
    plotter = Plotter(df, "x", "school")
    assert plotter.category_values() == ["A", "B", "C"]

def test_hue_values(df):
    plotter = Plotter(df, "x", "school", "km")
    assert plotter.hue_values() == ["Kvinna", "Man"]

@mock.patch('click.plt.show')
def test_boxplot_subplots(mock_show, df):
    plotter = Plotter(df, "x", "school", "km")
    with mock.patch('click.plt.subplots') as mockplots:
        mockplots.return_value = mock.Mock(), mock.Mock()
        plotter.boxplot()
        mockplots.assert_called_once()

@mock.patch('click.plt.show')
def test_boxplot_seaborn(mock_show, df):
    plotter = Plotter(df, "x", "school", "km")
    with mock.patch('click.sns.boxplot') as mockplot:
        plotter.boxplot()
        mockplot.assert_called_once_with(
            data=plotter.df, x="x", y="school", hue="km",
            whis=(10,90), order=["A", "B", "C"], 
            hue_order=["Kvinna", "Man"]
        )

def test_boxplot_show(df):
    plotter = Plotter(df, "x", "school", "km")
    with mock.patch('click.plt.show') as mockshow:
        plotter.boxplot()
        mockshow.assert_called_once()

def test_hover(df):
    hover = lambda: None
    plotter = Plotter(df, "x", "school", "km", on_hover=hover)
    assert plotter.on_hover == hover
    assert plotter.on_hover == hover

def test_annotate(df):
    plotter = Plotter(df, "x", "school", "km", annotate=('Skola', 'x'))
    assert plotter.annotate == ('Skola', 'x')

def test_get_row_1(df):
    Event = namedtuple('event', ['xdata', 'ydata'])
    plotter = Plotter(df, "x")
    row = plotter.get_row(Event(30799, 0))
    pdt.assert_series_equal(row, df.loc[1])
