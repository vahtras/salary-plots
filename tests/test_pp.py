import sys
import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

import click

Event = namedtuple('event', ['xdata', 'ydata'])

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
