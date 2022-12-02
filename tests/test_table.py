from collections import namedtuple
import pandas as pd
import pandas.testing as pdt

from catplot import plotters

Event = namedtuple("event", ["xdata", "ydata"])


# @pytest.mark.skip('fixme')
def test_tabular(active):
    plotter = plotters.Plotter(active, "kr")
    calculated = plotter.table().astype(int)
    expected = pd.DataFrame(
        [[10, 32568, 4663, 22732, 28575, 30083, 33619, 35306, 36213, 39648]],
        columns=[
            "count", "mean", "std", "min", "10%", "25%", "50%", "75%", "90%",
            "max",
        ],
        index=pd.Index(['Alla'], name='alla')
    )

    pdt.assert_frame_equal(calculated, expected)


def test_tabluar_grouped(active):
    plotter = plotters.Plotter(active, "kr", categorical="km")
    calculated = plotter.table().astype(int)
    expected = pd.DataFrame(
        [
            [6, 31144, 4673, 22732, 26288, 30083, 31961, 34482, 35182, 35430],
            [4, 34705, 4323, 29225, 30692, 32893, 34974, 36786, 38503, 39648],
            [10, 32568, 4663, 22732, 28575, 30083, 33619, 35306, 36213, 39648],
        ],
        columns=[
            "count", "mean", "std", "min", "10%", "25%", "50%", "75%", "90%",
            "max"
        ],
        index=pd.Index(['F', 'M', 'Alla'])
    )
    pdt.assert_frame_equal(calculated, expected)
