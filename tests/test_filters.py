import pytest
from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

from catplot import main, util

Event = namedtuple('event', ['xdata', 'ydata'])


def test_get_0(df):
    calculated = util.process_filters(df, ("kr=0",))
    expected = pd.DataFrame(dict(kr=[0], km=['O'], school=['D']), index=[5])
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
    calculated = util.process_filters(df, ("school@C:D",))
    expected = df[df.school.isin(['C', 'D'])]
    pdt.assert_frame_equal(calculated, expected)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("school=A", "A"),
        ("date>2018-10-01", "2018-10-01"),
        ("Chefsbef/annan bef=Chef (1)", "Chef (1)"),
        ("Grupp.nivå=4", "4"),
        ("Benämning@Arb:Tj,_folk", "Arb:Tj, folk"),
    ],
    ids=["=", ">", "()", "G", "@"])
def test_filter_values(test_input, expected):
    assert util.filter_values(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("school=A", "school"),
        ("date>2018-10-01", "date"),
        ("Chefsbef/annan bef=Chef (1)", "Chefsbef/annan bef"),
        ("Grupp.nivå=4", "Grupp.nivå"),
        ("Benämning@Arb:Tj", "Benämning"),
    ],
    ids=["=", ">", "()", "G", "@"])
def test_filter_keys(test_input, expected):
    assert util.filter_keys(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (["school=A"], {"school": "A"}),
        (["date>2018-10-01"], {"date": "2018-10-01"}),
        (["Chefsbef/annan bef=Chef (1)"], {"Chefsbef/annan bef": "Chef (1)"}),
        (["Grupp.nivå=4"], {"Grupp.nivå": "4"}),
        (["Benämning@Arb:Tj,_folk"], {"Benämning": ["Arb", "Tj, folk"]}),
    ],
    ids=["=", ">", "()", "G", "@"])
def test_filter_dict(test_input, expected):
    assert util.filter_dict(test_input) == expected
