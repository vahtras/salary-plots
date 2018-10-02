import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .plotters import BoxPlotter, PointPlotter

def box_demo():
    """
    Boxplot demo
    """
    sample = 10
    values = np.random.randint(20000, 40000, sample)
    genders = np.random.choice(['Kvinna', 'Man'], sample)
    units = np.random.choice(['A', 'B', 'C'], sample)

    df = pd.DataFrame(dict(values=values, genders=genders, units=units))

    box_plotter = BoxPlotter(
        df, 'values', categorical='genders', hue='units',
        annotate=('units', 'values', 'genders')
    )
    box_plotter.plot()
    box_plotter.ax.set_title("Box plot demo")
    plt.show()

def point_plot_demo():
    """
    Pointplot demo
    """
    sample = 10
    values = np.random.randint(20000, 40000, sample)
    genders = np.random.choice(['Kvinna', 'Man'], sample)
    units = np.random.choice(['A', 'B', 'C'], sample)

    df = pd.DataFrame(dict(values=values, genders=genders, units=units))

    point_plotter = PointPlotter(
        df,
        numerical='values',
        categorical='genders',
        annotate=('units', 'values', 'genders')
    )
    point_plotter.plot()
    point_plotter.ax.set_title("Point plot demo")
    plt.show()
