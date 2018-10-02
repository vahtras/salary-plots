import sys
import unittest.mock as mock
from catplot.click import main

@mock.patch('catplot.click.plt.show')
def test_boxplot(mock_show):
    sys.argv[1:] = [
        '--data', 'ftests/sample.csv',
        '--num', 'Lon',
        '--plot-type', 'box',
        '--title', 'POSTDOKTOR', '--table'
    ]
    with mock.patch('catplot.plotters.sns.boxplot') as mock_plot:
        main()
        assert mock_plot.called
    
@mock.patch('catplot.click.plt.show')
def test_pointplot(mock_show):
    sys.argv[1:] = [
        '--data', 'ftests/sample.csv',
        '--num', 'Lon',
        '--plot-type', 'point',
        '--title', 'POSTDOKTOR', '--table'
    ]
    with mock.patch('catplot.plotters.sns.stripplot') as mock_plot:
        main()
        assert mock_plot.called
