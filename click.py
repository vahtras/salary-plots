#!/usr/bin/env python 
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Plotter:
    def __init__(
        self, df, x, 
        category=None, hue=None, annotate=()
        ):
        self.df = df.copy()
        self.x = x
        self.category = category
        self.hue = hue
        self.annotate = annotate
        self.df["y"] = self.set_y()

    def category_values(self):
        if self.category is None:
            return []
        return sorted(list(self.df[self.category].dropna().unique()))

    def hue_values(self):
        if self.hue is None:
            return []
        return sorted(list(self.df[self.hue].dropna().unique()))

    def plot(self, **kwargs):
        self.fig, self.ax = plt.subplots()
        sns.boxplot(
            data=self.df, x=self.x, y=self.category, hue=self.hue,
            whis=(10, 90), order=self.category_values(),
            hue_order=self.hue_values()
        )
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self)

        plt.title(kwargs.get('title'))
        #plt.show()

    def get_row(self, event):
        if event.xdata is not None and event.ydata is not None:
            is_near_x = (self.df[self.x] - event.xdata)**2 < 10000
            is_near_y = (self.df.y - event.ydata)**2 < 0.1
            selected = is_near_x & is_near_y
            if selected.any():
                return self.df[selected].iloc[0]

    def set_y(self):
        """
        set expected y coordinate of categorical data point
        """
        if self.category is None:
            return pd.Series(len(self.df)*[.0], index=self.df.index)
        y_labels = sorted(list(self.df[self.category].unique()))
        y_values = pd.Series(
            (y_labels.index(row[self.category]) 
            if pd.notnull(row[self.category]) else -1
            for _, row in self.df.iterrows()) ,
            index=self.df.index
        )
        if self.hue:
            y_values += self.y_shift()
        return y_values 

    def y_shift(self):
        if self.hue:
            y_sublabels = sorted(list(self.df[self.hue].unique()))
            y_subvalues = pd.Series(
                (y_sublabels.index(row[self.hue])
                for _, row in self.df.iterrows()),
                index=self.df.index
            )
            multiplicity = len(y_sublabels)
            l = (multiplicity-1)/2
            y_shift = (y_subvalues-l)*.8/multiplicity
            return y_shift
        else:
            return pd.Series(len(self.df)*[0.], index=self.df.index)

    def __call__(self, event):
        row = self.get_row(event)
        if row is not None:
            fig = plt.gcf()
            ax = plt.gca()
            ax.annotate(
                "\n".join(
                        f"{row[k]}"
                        for k in self.annotate
                        if pd.notnull(row[k]) and row[k] != 0
                ),
                xy=(row[self.x], row.y),
                xytext=(20, 20),
                textcoords="offset points",
                bbox={"boxstyle": "square", "fc": "w", "lw": 2, "pad": 0.6},
                arrowprops={'arrowstyle': '->'},
            )
            fig.canvas.draw_idle()

    def on_click(self, event):
        print(event.xdata, event.ydata)

class BoxPlotter(Plotter):
    pass

class PointPlotter:
    def __init__(self, df, numerical="Månadslön", categorical="Kön", annotate=None):
        self.df = df
        self.numerical = numerical
        self.categorical = categorical
        if annotate is None:
            self.annotate = (numerical, categorical)
        else:
            self.annotate = annotate

    def plot(self):
        self.sorted = self.df.sort_values(
            self.numerical
        ).reset_index(drop=True)
        sns.stripplot(
            data=self.sorted,
            x=self.sorted.index,
            y=self.numerical,
            hue=self.categorical,
            ).set_xticklabels("")
        ax = plt.gca()
        fig = plt.gcf()
        ax.set_xticks([])
        fig.canvas.mpl_connect('motion_notify_event', self)

    def __call__(self, event):
        row = self.get_row(event)
        if row is not None:
            fig = plt.gcf()
            ax = plt.gca()
            ax.annotate(
                "\n".join(
                        f"{row[k]}"
                        for k in self.annotate
                        if pd.notnull(row[k]) and row[k] != 0
                ),
                xy=(row.name, row[self.numerical]),
                xytext=(20, 20),
                textcoords="offset points",
                bbox={"boxstyle": "square", "fc": "w", "lw": 2, "pad": 0.6},
                arrowprops={'arrowstyle': '->'},
            )
            fig.canvas.draw_idle()

    def get_row(self, event):
        if event.xdata:
            nearest_x = int(round(event.xdata))
            nearest_y = self.sorted.loc[nearest_x, self.numerical]
            diff_y = abs(event.ydata - nearest_y)
            if diff_y < 1000:
                return self.sorted.loc[nearest_x]
        
        

    
def main():

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

    args = parser.parse_args()

    if args.box_demo:
        box_demo()

    if args.box:
        if not args.num and not args.cat:
            raise Exception
        df = pd.read_csv(args.csv)
        import pdb; pdb.set_trace()
        bp = BoxPlotter(
            df,
            args.num,
            category=args.cat,
            annotate=args.annotate
        )
        bp.plot()
        plt.show()

    if args.point_plot_demo:
        point_plot_demo()

    if args.point_plot:
        if args.csv:
            df = pd.read_csv(args.csv)
            pp = PointPlotter(
                df,
                args.num,
                args.cat
            )
            pp.plot()
            plt.show()

        if args.xl:
            df = pd.read_excel(args.xl)
            pp = PointPlotter(
                df,
                args.num,
                args.cat
            )
            pp.plot()
            plt.show()

def box_demo():
    sample = 10
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)

    df = pd.DataFrame(dict(x=x, km=km, school=school))

    pl = BoxPlotter(
        df, 'x', category='school', hue='km',
        #on_hover=hover,
        annotate=('school', 'x', 'km')
    )
    pl.plot()
    plt.show()

def point_plot_demo():
    sample = 10
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)

    df = pd.DataFrame(dict(x=x, km=km, school=school))

    pl = PointPlotter(
        df,
        numerical='x',
        categorical='km',
        #on_hover=hover,
        annotate=('school', 'x', 'km')
    )
    pl.plot()
    plt.show()

if __name__ == "__main__":
    main()
