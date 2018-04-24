import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def main(
        df, x, category, hue=None, annotate=None,
        on_hover=None, on_click=None, boxplot=True,
        **kwargs
        ):
    category_values = sorted(list(df[category].dropna().unique()))
    hue_values = None
    if hue:
        hue_values = sorted(list(df[hue].unique()))

    fig, ax = plt.subplots()
    if boxplot:
        sns.boxplot(
            data=df, x=x, y=category, hue=hue,
            whis=(10, 90),
            orient='h',
            order=category_values,
            hue_order=hue_values,
            )
    else:
        df_sorted = pointplot(df, x, hue, kwargs.get('palette'))
 
    ax.set_title(kwargs.get('title', None))
    vlines = kwargs.get('vlines', None)
    if vlines:
        _, ymax = plt.ylim()
        for what, where in vlines.items():
            ax.axvline(where, color='g')
            #xticks.append(x)
            #xlabels.append(labx)
            ax.annotate(f"{what}", (where, ymax), rotation=0)
    text = kwargs.get('text', None)
    if text:
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        ax.text(1.05, 0.50, text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)


    if annotate is not None:
        if boxplot:
            if on_hover is None:
                on_hover = hover
            on_hover._df = set_y(df, category, hue)
            on_hover._df['x'] = df[x]
        else:
            on_hover._df = df_sorted
            on_hover._df['y'] = df_sorted.x
            on_hover._df['x'] = df_sorted.index
            print(on_hover._df)
        on_hover._annotate = annotate
        id = fig.canvas.mpl_connect('motion_notify_event', on_hover)

    on_click._df = on_hover._df
    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.show()

def set_y(df, y_label, y_sublabel=None):
    _df = df.copy()
    y_labels = sorted(list(_df[y_label].unique()))
    y_values = [y_labels.index(row[y_label]) if pd.notnull(row[y_label])  else -1 for _, row in _df.iterrows() ]
    _df["y"] = y_values
    if y_sublabel:
        y_sublabels = sorted(list(_df[y_sublabel].unique()))
        y_subvalues = [
            y_sublabels.index(row[y_sublabel]) for _, row in _df.iterrows()
        ]
        _df["dy"] = y_subvalues
        _df.dy -= (len(y_sublabels)-1) / 2
        _df.dy *= .4
        _df.y += _df.dy
    return _df

def ignore(event):
    pass

def get_row(event, df):
    if event.xdata is not None and event.ydata is not None:
        is_near_x = (df.x - event.xdata)**2 < 10000
        is_near_y = (df.y - event.ydata)**2 < 0.1
        selected = is_near_x & is_near_y
        if selected.any():
            return df[selected].iloc[0]

def get_row_pp(event, df):
    if event.xdata is not None and event.ydata is not None:
        #print("x values: ", df.x, event.xdata)
        #print("y values: ", df.y, event.ydata)
        is_near_x = (df.x - event.xdata)**2 < 0.5
        is_near_y = (df.y - event.ydata)**2 < 10000
        selected = is_near_x & is_near_y
        if selected.any():
            return df[selected].iloc[0]
        
def hover(event):
    if True:
        row = get_row(event, hover._df)
    else:
        row = get_row_pp(event, hover._df)
    if row is not None:
        fig = plt.gcf()
        ax = plt.gca()
        ax.annotate(
            "\n".join(f"{row[k]}" for k in hover._annotate if pd.notnull(row[k]) and row[k] != 0),
            xy=(row.x, row.y),
            xytext=(20, 20),
            textcoords="offset points",
            bbox={"boxstyle": "square", "fc": "w", "lw": 2, "pad": 0.6},
            arrowprops={'arrowstyle': '->'},
        )
        fig.canvas.draw_idle()


def pointplot(df, y, hue, palette):
    df_sorted = df.sort_values(y).reset_index(drop=True)
    sns.stripplot(
        data=df_sorted, y=y, x=df_sorted.index, hue=hue,
        palette=palette
    ).set_xticklabels("")
    df_sorted['y'] = df[y]
    return df_sorted

if __name__ == "__main__":
    sample = 10
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['Kvinna', 'Man'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)
    oldschool = np.random.choice(['a', 'b', 'c'], sample)

    uid1 = np.arange(sample)
    uid2 = uid1.copy()
    np.random.shuffle(uid2)

    df = pd.DataFrame(dict(x=x, Skola=school, Kön=km, uid=uid1))
    print(df)

    def print_xy(event):
        print(event.xdata, event.ydata)

    boxplot = False
    def print_row(event):
        if boxplot:
            row = get_row(event, print_row._df)
        else:
            row = get_row_pp(event, print_row._df)
        print(row)
    print_row._df = df
    hover._df = df

    main(
        df,
        'x', 'Skola', 'Kön',
        annotate=('Skola', 'x', 'Kön'),
        on_click=print_row,
        on_hover=hover,
        boxplot=True,
        palette={'Kvinna': 'Red', 'Man': 'Blue'},
        title="Pointplot",
    )
