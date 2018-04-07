import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def main(df):
    y1, y2 = range(2)
    #print(df)

    fig, ax = plt.subplots()
    sns.boxplot(data=df, x=x, y=ab, whis=(10, 90), orient='h', order=('A', 'B'))

    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            is_near = (df.x - event.xdata)**2 < .01
            is_A = (df.ab == "A") & (event.ydata < .1)
            sel = is_A & is_near
            if sel.any():
                #print(df[sel])
                for i, row in df[sel].iterrows():
                    ax.annotate(
                        f"{row.ab}\n{row.x}",
                        xy=(row.x, y1),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox={"boxstyle": "round", "fc": "w", "lw": 2},
                        arrowprops={'arrowstyle': '->'},
                    )
                fig.canvas.draw_idle()

    cid = fig.canvas.mpl_connect('motion_notify_event', onclick)
    fig.suptitle(', '.join(map(str, sorted(x))))
    plt.show()

if __name__ == "__main__":
    x = np.random.randint(1, 100, 20)
    ab = np.random.choice(list('AB'), 20)
    df = pd.DataFrame(dict(x=x, ab=ab))

    sys.exit(main(df))
