#!/usr/bin/env python
"""
Generate seaborn boxplots and strip plots with annotations
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from configparser import ConfigParser
from .demos import *

def process_data(data):
    h, e = os.path.splitext(data)
    if e == '.csv':
        df = pd.read_csv(data)
    elif e == '.xlsx':
        df = pd.read_excel(data)
    else:
        raise Exception(f'Unknown file format: {e}')
    return df
        
def process_filters(df, filters):
    for kv in filters:
        if '!=' in kv:
            k, v = kv.split('!=')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] != v]
        elif '=' in kv:
            k, v = kv.split('=')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] == v]
        elif '>' in kv:
            k, v = kv.split('>')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] > v]
        elif '<' in kv:
            k, v = kv.split('>')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] < v]
    return df

def get_config(args=None, ini=None):
    cfg = os.environ
    if ini:
        config = ConfigParser()
        config.read(ini)
        cfg = {**cfg, **config['DEFAULT']}
    if args:
        cfg = {**cfg, **vars(args)}
    return cfg

def main():
    """
    Main driver for annotated plots
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Data file (excel/csv)')
    parser.add_argument('--box-plot-demo', action='store_true', help='Box demo')
    parser.add_argument('--point-plot-demo', action='store_true', help='Point demo')
    parser.add_argument('--box-plot', action='store_true', help='Box plot')
    parser.add_argument('--point-plot', action='store_true', help='Point plot')
    parser.add_argument('--num', help='Numerical label')
    parser.add_argument('--cat', help='Categorical label')
    parser.add_argument('--annotate', nargs='+', default=(), help='pop-up info')
    parser.add_argument('--filters', nargs='+', default=[], help='filter data')
    parser.add_argument('--title', default="", help='Pass title to fig')
    parser.add_argument('--table', action='store_true', help='Print table')
    

    args = parser.parse_args()
    print(args)

    if args.box_plot_demo:
        box_demo()
        return

    if args.point_plot_demo:
        point_plot_demo()
        return

    if not args.data:
        return

    df = process_data(args.data)

    df = df[df[args.num] > 0]
    df = process_filters(df, args.filters)

    if args.box_plot:
        box_plotter = BoxPlotter(
            df,
            args.num,
            categorical=args.cat,
            annotate=args.annotate,
        )
        if args.table:
            print(box_plotter.table())
        box_plotter.plot(title=args.title)
        plt.show()


    if args.point_plot:
        point_plotter = PointPlotter(
            df,
            args.num,
            categorical=args.cat,
            annotate=args.annotate,
            title=args.title
        )
        point_plotter.plot(title=args.title)
        if args.table:
            print(point_plotter.table())
        plt.show()

if __name__ == "__main__":
    main()
