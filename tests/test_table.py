import sys
import pytest
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

import click

Event = namedtuple('event', ['xdata', 'ydata'])
   
def test_tabluar(active):
    plotter = click.Plotter(active, 'kr')
    calculated = plotter.table()
    expected = pd.DataFrame(
        dict(kr=[10, 32568, 22732, 28575, 30083, 33619, 35306, 36213, 39648]),
        index=('count', 'mean', 'min', '10%', '25%', '50%', '75%', '90%', 'max')
    )
    pdt.assert_frame_equal(calculated, expected)
