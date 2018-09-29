import sys
import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

import click

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
            kr=[22732, 30799, 29845, 39648, 33123, 0,
               29225, 34116, 34935, 35430, 35832],
            km=['Kvinna', 'Kvinna', 'Kvinna', 'Man', 'Kvinna', 'Barn',
                'Man', 'Man', 'Kvinna', 'Kvinna', 'Man' ],
            school=['B', 'B', 'B', 'A', 'B', 'D',
                    'A', 'A', 'B', 'C', 'A'],
        )
    )
    return _df[_df.kr > 0]
   
def test_pp_default_setup(df):
    plotter = click.PointPlotter(df, "Salary", categorical="Gender")
    assert plotter.df is df
    assert plotter.numerical == "Salary"
    assert plotter.categorical == "Gender"

def test_pp_plot(df):
    #df_sorted = pd.read_csv('test_pp_plot.csv')
    pp = click.PointPlotter(df, numerical='kr', categorical='km')

    with mock.patch('click.sns.stripplot') as mock_stripplot:
        pp.plot()

    mock_stripplot.assert_called()

def test_read_csv_data():
    with mock.patch('click.pd.read_csv') as mock_csv:
        click.process_data('exported.csv')

def test_read_xl_data():
    with mock.patch('click.pd.read_excel') as mock_xl:
        click.process_data('exported.xlsx')
