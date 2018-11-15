import sys
import pytest
from unittest import mock
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

from catplot import plotters, main, util

Event = namedtuple('event', ['xdata', 'ydata'])
   
def test_get_0(df):
    calculated = util.process_filters(df, ("kr=0",))
    expected = pd.DataFrame(dict(kr=[0], km=['Barn'], school=['D']), index=[5])
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0a(df):
    calculated = util.process_filters(df, ("kr!=0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0b(df):
    calculated = main.process_filters(df, ("kr>0",))
    expected = df[df.kr > 0]
    pdt.assert_frame_equal(calculated, expected)

def test_rm_0c(df):
    calculated = util.process_filters(df, ("kr<25000",))
    expected = df[df.kr < 25000]
    pdt.assert_frame_equal(calculated, expected)

def test_isin(df):
    calculated = util.process_filters(df, ("school@C,D",))
    expected = df[df.school.isin(['C','D'])]
    pdt.assert_frame_equal(calculated, expected)

@pytest.mark.parametrize("test_input,expected",[
    ("school=A", "A"),
    ("date>2018-10-01", "2018-10-01"),
], ids=["=", ">"])
def test_filter_values(test_input, expected):
    assert util.filter_values(test_input) == expected
