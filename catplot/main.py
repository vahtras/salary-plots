#!/usr/bin/env python
"""
Generate seaborn boxplots and strip plots with annotations
"""
import os
import re
import json
import matplotlib.pyplot as plt
import pandas as pd
from configparser import ConfigParser
from .demos import box_demo, point_plot_demo
from .plotters import plotters
from .util import process_filters, filter_values


def process_data(data):
    h, e = os.path.splitext(data)
    if e == '.csv':
        df = pd.read_csv(data)
    elif e == '.xlsx':
        df = pd.read_excel(data)
    else:
        raise Exception(f'Unknown file format: {e}')
    return df


def get_config(args=None, ini=None):
    cfg = os.environ
    if ini:
        config = ConfigParser()
        config.read(ini)
        cfg = {**cfg, **config['DEFAULT']}
        if cfg.get('plot_type') in config.sections():
            cfg = {**cfg, **config[cfg['plot_type']]}
        elif args:
            if args.plot_type in config.sections():
                cfg = {**cfg, **config[args.plot_type]}

        if 'filters' in cfg:
            cfg['filters'] = cfg['filters'].split('\n')
        if 'annotate' in cfg:
            cfg['annotate'] = cfg['annotate'].split('\n')
        if 'palette' in cfg:
            cfg['palette'] = {
                k: v.strip() for k, v in (
                    line.split(':') for line in cfg['palette'].split('\n')
                    if line
                    )
            }
    if args:
        kwargs = {k: v for k, v in vars(args).items() if v is not None}
        # Do not overwrite filters, update
        if 'filters' in cfg and 'filters' in kwargs:
            kwargs['filters'] += cfg['filters']
        cfg = {**cfg, **kwargs}
    return cfg


def get_args():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Data file (excel/csv)')
    parser.add_argument(
        '--box-plot-demo', action='store_true', help='Box demo'
    )
    parser.add_argument(
        '--point-plot-demo', action='store_true', help='Point demo'
    )
    parser.add_argument(
        '--plot-type', choices=('box', 'point'), help='Plot type'
    )
    parser.add_argument('--num', help='Numerical label')
    parser.add_argument('--cat', help='Categorical label')
    parser.add_argument(
        '--annotate', nargs='+', default=(), help='pop-up info'
    )
    parser.add_argument('--filters', nargs='+', default=[], help='filter data')
    parser.add_argument('--show', nargs='+', default=[], help='filter data')
    parser.add_argument('--title', default=None, help='Pass title to fig')
    parser.add_argument('--table', type=int, default=None, help='Print table')
    parser.add_argument('--palette', default=None, help='Colors')
    parser.add_argument(
        '--yo', nargs='+', default=[], type=int, help='filter data'
    )

    args = parser.parse_args()
    return args


def main():
    """
    Main driver for annotated plots
    """

    cfg = get_config(get_args(), ini='config.ini')

    if cfg.get('box_plot_demo'):
        box_demo()
        return

    if cfg.get('point_plot_demo'):
        point_plot_demo()
        return

    if not cfg['data']:
        print("No data")
        return

    if cfg.get('palette'):
        if isinstance(cfg['palette'], str):
            palette = json.loads(cfg['palette'])
        else:
            palette = cfg['palette']
    else:
        palette = None

    df = process_data(cfg['data'])
    df = process_filters(df, cfg.get('filters', []))

    plotter = plotters[cfg['plot_type']](
        df,
        cfg['num'],
        categorical=cfg.get('cat'),
        annotate=cfg.get('annotate'),
        palette=palette,
    )

    cfg['title'] = cfg.get('title', ' '.join(cfg.get('filters', [])))

    plotter.plot(
        **cfg,
    )

    fig = plt.gcf()
    plt.show()

    figure_file = f"{cfg['plot_type']}"

    values = [filter_values(f) for f in cfg.get('filters', [])]
    figure_file += f"-{'_'.join(values)}"
    csv_file = f"{'_'.join(values)}"

    figure_file += f"-{cfg['num']}"
    if cfg.get('cat'):
        cats = re.sub('/', ':', f"-{cfg.get('cat', '')}")
        figure_file += cats
        csv_file += cats
    figure_file += ".png"
    csv_file += ".csv"

    fig.savefig(figure_file)

    if cfg.get('table') is not None:
        precision = cfg.get('table')
        plotter.table().to_csv(csv_file)
        if precision > 0:
            print(plotter.table().round(precision))
        else:
            print(plotter.table().astype(int))


if __name__ == "__main__":
    main()
