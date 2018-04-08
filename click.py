import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_y(df, y_label, y_sublabel=None):
    _df = df.copy()
    #print(_df)
    labels = sorted(list(_df[y_label].unique()))
    y_values = [labels.index(row[y_label]) for _, row in _df.iterrows()]
    _df["y"] = y_values
    if y_sublabel:
        sublabels = sorted(list(_df[y_sublabel].unique()))
        y_subvalues = [
            sublabels.index(row[y_sublabel]) for _, row in _df.iterrows()
        ]
        _df["dy"] = y_subvalues
        _df.dy -= (len(sublabels)-1) / 2
        _df.dy *= .4
        _df.y += _df.dy
    #print(_df)
    return _df
        

def main(df, x, category, hue=None, annotate=None, on_click=None):
    category_values = sorted(list(df[category].dropna().unique()))
    hue_values = None
    if hue:
        hue_values = sorted(list(df[hue].unique()))

    fig, ax = plt.subplots()
    sns.boxplot(
        data=df, x=x, y=category, hue=hue,
        whis=(10, 90),
        orient='h',
        order=category_values,
        hue_order=hue_values
        )

    def hover(event):
        if event.xdata is not None and event.ydata is not None:
            is_near_x = (hover._df[x] - event.xdata)**2 < 10000
            is_near_y = (hover._df.y - event.ydata)**2 < 0.1
            selected = is_near_x & is_near_y
            if selected.any():
                for i, row in hover._df[selected].iterrows():
                    ax.annotate(
                        "\n".join(f"{row[k]}" for k in annotate if pd.notnull(row[k]) and row[k] != 0),
                        xy=(row[x], row.y),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox={"boxstyle": "round", "fc": "w", "lw": 2},
                        arrowprops={'arrowstyle': '->'},
                    )
                fig.canvas.draw_idle()

    if annotate is not None:
        hover._df = set_y(df, category, hue)
        cid = fig.canvas.mpl_connect('motion_notify_event', hover)


    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sample = 100
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)
    df = pd.DataFrame(dict(x=x, Skola=school, Kön=km))

    def print_xy(event):
        print(event.xdata, event.ydata)

    sys.exit(main(df[df.Skola.isin(['B', 'C'])], 'x', 'Skola', 'Kön', annotate=('Skola', 'x', 'Kön'), on_click=print_xy))
