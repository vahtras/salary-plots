import sys
import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

import click

Event = namedtuple('event', ['xdata', 'ydata'])
   
def test_get_0(df):
    calculated = click.process_filters(df, ("kr=0",))
    expected = pd.DataFrame(dict(kr=[0], km=['Barn'], school=['D']), index=[5])
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0a(df):
    calculated = click.process_filters(df, ("kr!=0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0b(df):
    calculated = click.process_filters(df, ("kr>0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)
