import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def main(df, x, category):
    category_values = sorted(list(df[category].unique()))
    y = range(len(category_values))
    #print(df)

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x=x, y=category, whis=(10, 90), orient='h',
        order=category_values
        )

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            is_near = (df.x - event.xdata)**2 < .01
            for iv, cv in enumerate(category_values):
                is_category = (df[category] == cv) & (
                abs(event.ydata-y[iv]) < .1
                )
                sel = is_category & is_near
                if sel.any():
                    #print(df[sel])
                    for i, row in df[sel].iterrows():
                        ax.annotate(
                            f"{row[category]}\n{row[x]}",
                            xy=(row[x], y[iv]),
                            xytext=(20, 20),
                            textcoords="offset points",
                            bbox={"boxstyle": "round", "fc": "w", "lw": 2},
                            arrowprops={'arrowstyle': '->'},
                        )
                    fig.canvas.draw_idle()

    cid = fig.canvas.mpl_connect('motion_notify_event', onclick)
    plt.show()

if __name__ == "__main__":
    x = np.random.randint(1, 100, 20)
    ab = np.random.choice(list('AB'), 20)
    df = pd.DataFrame(dict(x=x, category=ab))

    sys.exit(main(df, 'x', 'category'))
