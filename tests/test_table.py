import sys
import pytest
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

import click

Event = namedtuple('event', ['xdata', 'ydata'])
   
def test_tabular(active):
    plotter = click.Plotter(active, 'kr')
    calculated = plotter.table()
    expected = pd.Series(
        [10, 32568, 22732, 28575, 30083, 33619, 35306, 36213, 39648],
        index=('count', 'mean', 'min', '10%', '25%', '50%', '75%', '90%',
'max'),
        name='kr'
    )
    pdt.assert_series_equal(calculated, expected)

def test_tabluar_grouped(active):
    plotter = click.Plotter(active, 'kr', categorical='km')
    calculated = plotter.table()
    expected = pd.DataFrame(
        data=dict(
            Kvinna=[6, 31144, 22732, 26288, 30083, 31961, 34482, 35182, 35430],
               Man=[4, 34705, 29225, 30692, 32893, 34974, 36786, 38503, 39648]
        ),
        index=['count', 'mean', 'min', '10%', '25%', '50%', '75%', '90%', 'max']
    ).T
    expected.index.name = 'km'
    pdt.assert_frame_equal(calculated, expected)
