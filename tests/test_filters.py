import sys
import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

from catplot import plotters, main

Event = namedtuple('event', ['xdata', 'ydata'])
   
def test_get_0(df):
    calculated = main.process_filters(df, ("kr=0",))
    expected = pd.DataFrame(dict(kr=[0], km=['Barn'], school=['D']), index=[5])
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0a(df):
    calculated = main.process_filters(df, ("kr!=0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0b(df):
    calculated = main.process_filters(df, ("kr>0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)

def test_isin(df):
    calculated = main.process_filters(df, ("school in C D",))
    expected = df[df.school.isin(['C','D'])]
    pdt.assert_frame_equal(calculated, expected)
