#!/usr/bin/env python
"""
Generate seaborn boxplots and strip plots with annotations
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plotter:
    """
    Base plotter class

    Implements generic __call__
    Subclasses should implement

        plot(self, **kwargs)
        get_row(self, event)
        get_coordinate(self, row)
    """

    def __init__(self, df, numerical, **kwargs):
        self.df = df
        self.numerical = numerical

        default = dict(
            categorical=None,
            annotate=None
            )
        settings = {**default, **kwargs}
        self.categorical = settings.get('categorical')
        self.annotate = settings.get('annotate', numerical)
        self.fig = None
        self.ax = None
        self.sorted = None

    def categorical_values(self):
        """
        Returns list of values associated with the categorical variable
        """
        if self.categorical is None:
            return []
        return sorted(list(self.df[self.categorical].dropna().unique()))

    def plot(self, **kwargs):
        "To be implemented by subclass"
        raise NotImplementedError

    def get_row(self, event):
        "To be implemented by subclass"
        raise NotImplementedError

    def get_coordinate(self, row):
        "To be implemented by subclass"
        raise NotImplementedError

    def __call__(self, event):
        """
        Generic method that allows interaction with mouse
        to display information about a data point
        """
        row = self.get_row(event)
        if row is not None:
            fig = plt.gcf()
            ax = plt.gca()
            if self.annotate:
                ax.annotate(
                    "\n".join(
                        f"{row[k]}"
                        for k in self.annotate
                        if pd.notnull(row[k]) and row[k] != 0
                    ),
                    xy=self.get_coordinate(row),
                    xytext=(20, 20),
                    textcoords="offset points",
                    bbox={"boxstyle": "square", "fc": "w", "lw": 2, "pad": 0.6},
                    arrowprops={'arrowstyle': '->'},
                )
            fig.canvas.draw_idle()

    def on_click(self, event):
        """
        Action when mouse is clicked
        """
        print(event.xdata, event.ydata)


class BoxPlotter(Plotter):
    """
    Generate interactive box plots with category and subcategory
    """

    def __init__(self, df, numerical, **kwargs):
        """
        Iniitalize for boxplot
        """
        super().__init__(df, numerical, **kwargs)
        self.hue = kwargs.get('hue')
        self.df["y"] = self.set_y()

    def hue_values(self):
        """
        Returns list of values associated with the subcategory (hue)
        """
        if self.hue is None:
            return []
        return sorted(list(self.df[self.hue].dropna().unique()))

    def plot(self, **kwargs):
        """
        Calls the Seaborn plot function and connects the plot for interactive
        with mouse
        """
        self.fig, self.ax = plt.subplots()
        sns.boxplot(
            data=self.df, x=self.numerical, y=self.categorical, hue=self.hue,
            whis=(10, 90), order=self.categorical_values(),
            hue_order=self.hue_values()
        )

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self)

        plt.title(kwargs.get('title'))
        #plt.show()

    def get_row(self, event):
        """
        Given the coordinates of the mouse the function returns a row in the
        dataframe matching the data point
        """
        row = None
        if event.xdata is not None and event.ydata is not None:
            is_near_x = (self.df[self.numerical] - event.xdata)**2 < 10000
            is_near_y = (self.df.y - event.ydata)**2 < 0.1
            selected = is_near_x & is_near_y
            if selected.any():
                row = self.df[selected].iloc[0]
        return row

    def set_y(self):
        """
        set expected y coordinate of categorical data point
        """
        if self.categorical is None:
            return pd.Series(len(self.df)*[.0], index=self.df.index)
        y_labels = sorted(list(self.df[self.categorical].unique()))
        y_values = pd.Series(
            (y_labels.index(row[self.categorical])
             if pd.notnull(row[self.categorical]) else -1
             for _, row in self.df.iterrows()
            ),
            index=self.df.index
        )
        if self.hue:
            y_values += self.y_shift()
        return y_values

    def y_shift(self):
        """
        update expected y coordinate for subcategorical data point
        """
        if self.hue:
            y_sublabels = sorted(list(self.df[self.hue].unique()))
            y_subvalues = pd.Series(
                (y_sublabels.index(row[self.hue])
                 for _, row in self.df.iterrows()
                ),
                index=self.df.index
            )
            multiplicity = len(y_sublabels)
            level = (multiplicity-1)/2
            level_shift = (y_subvalues-level)*.8/multiplicity
        else:
            level_shift = pd.Series(len(self.df)*[0.], index=self.df.index)

        return level_shift

    def get_coordinate(self, row):
        """
        Return coordinates of data point associated with a dataframe row
        """
        return (row[self.numerical], row.y)




class PointPlotter(Plotter):
    """
    Generate interactive point plots with color coded category
    """

    def plot(self, **kwargs):
        """
        Calls the Seaborn plot function and connects the plot for interactive
        with mouse
        """
        self.sorted = self.df.sort_values(
            self.numerical
        ).reset_index(drop=True)

        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        sns.stripplot(
            data=self.sorted,
            x=self.sorted.index,
            y=self.numerical,
            hue=self.categorical,
            ).set_xticklabels("")
        self.ax.legend(loc='upper left')

        self.ax.set_xticks([])
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self)

    def get_coordinate(self, row):
        """
        Return coordinates of data point associated with a dataframe row
        """
        return (row.name, row[self.numerical])

    def get_row(self, event):
        """
        Given the coordinates of the mouse the function returns a row in the
        dataframe matching the data point
        """
        row = None
        if event.xdata:
            nearest_x = int(round(event.xdata))
            nearest_y = self.sorted.loc[nearest_x, self.numerical]
            diff_y = abs(event.ydata - nearest_y)
            if diff_y < 1000:
                row = self.sorted.loc[nearest_x]
        return row

def main():
    """
    Main driver for annotated plots
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--box-demo', action='store_true', help='Box demo')
    parser.add_argument('--box', action='store_true', help='Box plot')
    parser.add_argument('--point-plot-demo', action='store_true', help='Point demo')
    parser.add_argument('--point-plot', action='store_true', help='Point plot')
    parser.add_argument('--csv', help='CSV file')
    parser.add_argument('--xl', help='excel file')
    parser.add_argument('--num', help='Numerical label')
    parser.add_argument('--cat', help='Categorical label')
    parser.add_argument('--annotate', nargs='+', default=(), help='pop-up info')
    parser.add_argument('--filters', nargs='+', default=[], help='filter data')
    

    args = parser.parse_args()

    if args.box_demo:
        box_demo()

    if args.point_plot_demo:
        point_plot_demo()

    if args.csv:
        df = pd.read_csv(args.csv)
    elif args.xl:
        df = pd.read_excel(args.xl)
    else:
        print("No data file")
        return

    df = df[df[args.num] > 0]
    for kv in args.filters:
        if '!=' in kv:
            k, v = kv.split('!=')
            try:
                v = int(v)
            except ValueError:
                pass
            df = df[df[k] == v]

        if '=' in kv:
            k, v = kv.split('=')
            try:
                v = int(v)
            except ValueError:
                pass

            df = df[df[k] == v]
    

    if args.box:
        box_plotter = BoxPlotter(
            df,
            args.num,
            categorical=args.cat,
            annotate=args.annotate,
        )
        box_plotter.plot()
        plt.show()


    if args.point_plot:
        point_plotter = PointPlotter(
            df,
            args.num,
            categorical=args.cat,
            annotate=args.annotate,
        )
        point_plotter.plot()
        plt.show()

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
    plt.show()

if __name__ == "__main__":
    main()
