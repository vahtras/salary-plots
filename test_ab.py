import pytest
import numpy as np
import pandas as pd
import pandas.util.testing as pdt
import click

"""
      Kön Skola      x
0  Kvinna     B  22732
1  Kvinna     B  30799
2  Kvinna     B  29845
3     Man     A  39648
4  Kvinna     B  33123
5     Man     A  29225
6     Man     A  34116
7  Kvinna     B  34935
8  Kvinna     C  35430
9     Man     A  35832
"""


@pytest.fixture
def sample():
    samples = 10
    np.random.seed(0)
    x = np.random.randint(20000, 40000, samples)
    km = np.random.choice(['Kvinna', 'Man'], samples)
    school = np.random.choice(['A', 'B', 'C'], samples)
    df = pd.DataFrame(dict(x=x, Skola=school, Kön=km))
    return df

def test_init(sample):
    assert len(sample) == 10

def test_y_cat(sample):
    df = click.set_y(sample, 'Skola')
    assert  list(df.y) == [1., 1., 1., 0., 1., 0., 0., 1., 2. ,0.]

def test_y_subcat(sample):
    df = click.set_y(sample, 'Skola', 'Kön')
    pdt.assert_series_equal(
        df.y, pd.Series([.8, .8, .8, 0.2, .8, .2, .2, .8, 1.8 ,.2], name='y')
    )

def test_get_row(sample):
    from collections import namedtuple
    event = namedtuple("event", ["xdata", "ydata"])
    df = click.set_y(sample, 'Skola', 'Kön')
    pdt.assert_series_equal(
        click.get_row(event(29225, .2), df),
        df.loc[5]
    )
