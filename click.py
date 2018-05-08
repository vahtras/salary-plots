import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Plotter:
    def __init__(
        self, df, x, 
        category=None, hue=None, on_hover=None, on_click=None, annotate=()
        ):
        self.df = df.copy()
        self.x = x
        self.category = category
        self.hue = hue
        self.on_hover = on_hover
        self.on_click = print_xy
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

    def boxplot(self):
        self.fig, self.ax = plt.subplots()
        sns.boxplot(
            data=self.df, x=self.x, y=self.category, hue=self.hue,
            whis=(10, 90), order=self.category_values(),
            hue_order=self.hue_values()
        )
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self)
        plt.show()

    def get_row(self, event):
        if event.xdata is not None and event.ydata is not None:
            is_near_x = (self.df[self.x] - event.xdata)**2 < 10000
            is_near_y = (self.df.y - event.ydata)**2 < 0.1
            selected = is_near_x & is_near_y
            if selected.any():
                return self.df[selected].iloc[0]

    def set_y(self):
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

def print_xy(event):
    print(event.xdata, event.ydata)

if __name__ == "__main__":
    sample = 10
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)

    df = pd.DataFrame(dict(x=x, km=km, school=school))

    pl = Plotter(
        df, 'x', category='school', hue='km',
        #on_hover=hover,
        on_click=print_xy,
        annotate=('school', 'x', 'km')
    )
    pl.boxplot()
