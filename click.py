import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def set_y(df, y_label, y_sublabel=None):
    labels = sorted(list(df[y_label].unique()))
    y_values = (labels.index(row[y_label]) for _, row in df.iterrows())
    df["y"] = pd.Series(y_values)
    if y_sublabel:
        sublabels = sorted(list(df[y_sublabel].unique()))
        y_subvalues = (
            sublabels.index(row[y_sublabel]) for _, row in df.iterrows()
        )
        df["dy"] = pd.Series(y_subvalues)
        df.dy -= (len(sublabels)-1) / 2
        df.dy *= .4
        df.y += df.dy
        

def main(df, x, category, hue=None, annotate=None):
    category_values = sorted(list(df[category].unique()))
    hue_values = None
    if hue:
        hue_values = sorted(list(df[hue].unique()))
    set_y(df, category, hue)

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
            is_near_x = (df[x] - event.xdata)**2 < 1000
            is_near_y = (df.y - event.ydata)**2 < 0.1
            selected = is_near_x & is_near_y
            if selected.any():
                for i, row in df[selected].iterrows():
                    ax.annotate(
                        "\n".join(str(row[k]) for k in annotate),
                        xy=(row[x], row.y),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox={"boxstyle": "round", "fc": "w", "lw": 2},
                        arrowprops={'arrowstyle': '->'},
                    )
                fig.canvas.draw_idle()

    if annotate is not None:
        cid = fig.canvas.mpl_connect('motion_notify_event', hover)

    def on_click(event):
        print(event.xdata, event.ydata)

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()

if __name__ == "__main__":
    sample = 100
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C', 'D'], sample)
    df = pd.DataFrame(dict(x=x, Skola=school, Kön=km))

    sys.exit(main(df, 'x', 'Skola', 'Kön', annotate=('Skola', 'x', 'Kön')))
