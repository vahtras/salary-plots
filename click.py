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
    def __init__(self, df, numerical="Månadslön", categorical="Kön"):
        self.df = df
        self.numerical = numerical
        self.categorical = categorical

    def plot(self):
        df_sorted = self.df[[self.numerical, self.categorical]].sort_values(
            self.numerical
        ).reset_index(drop=True)
        sns.stripplot(
            data=df_sorted,
            x=df_sorted.index,
            y=self.numerical,
            hue=self.categorical,
            )

    
def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--box-demo', action='store_true', help='Demo')
    parser.add_argument('--box', action='store_true', help='Demo')
    parser.add_argument('--csv', help='CSV file')
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

if __name__ == "__main__":
    main()
