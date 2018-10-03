import os
import argparse
import unittest.mock as mock
from catplot.main import get_config

def test_data_from_env():
    os.environ['data'] = 'export.xlsx'
    cfg = get_config()
    assert cfg['data'] == 'export.xlsx'

def test_data_from_cfg():
    os.environ['data'] = 'export.xlsx'
    with mock.patch('catplot.main.ConfigParser') as mock_parser:
        mock_parser.return_value = mock.MagicMock()
        mock_config = mock_parser()
        mock_config.__getitem__.side_effect = \
            lambda k: {'DEFAULT': {'data': 'alt.xlsx'}}[k]
        cfg = get_config(ini='config.ini')
        
    mock_config.read.assert_called_with('config.ini')
    assert cfg['data'] == 'alt.xlsx'

def test_data_from_cmdline():
    os.environ['data']= 'export.xlsx'
    parser = argparse.ArgumentParser()
    parser.add_argument('--data')
    args = parser.parse_args(['--data', 'alt2.xlsx'])
    cfg = get_config(args=args, ini=None)
    assert cfg['data'] == 'alt2.xlsx'
