import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .plotters import BoxPlotter, PointPlotter

def box_demo():
    """
    Boxplot demo
    """
    sample = 100
    values = np.random.randint(20000, 40000, sample)
    genders = np.random.choice(['Female', 'Male'], sample)
    units = np.random.choice(['Dept A', 'Dept B', 'Dept C'], sample)

    df = pd.DataFrame(dict(Value=values, Gender=genders, Unit=units))

    box_plotter = BoxPlotter(
        df, 'Value', categorical='Unit', hue='Gender',
        annotate=('Unit', 'Value', 'Gender')
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
    genders = np.random.choice(['Female', 'Male'], sample)
    units = np.random.choice(['Dept A', 'Dept B', 'Dept C'], sample)

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
