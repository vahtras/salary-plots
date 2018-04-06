import matplotlib.pyplot as plt
import numpy as np

x = np.random.randint(1, 100, 20)
y = 1

fig, ax = plt.subplots()
ax.boxplot(x, vert=False, whis=(10,90))

def onclick(event):
    #print(f"x={event.x} y={event.y} button={event.button}")
    #print(f"    xdata={event.xdata} ydata={event.ydata}")
    if event.xdata is not None and event.ydata is not None:
        ix = int(round(event.xdata))
        if ix in x and abs(event.ydata - y) < .01:
            print(f"Picked x={ix} y={event.ydata}")
            ax.annotate(
                f"{ix}", xy=(ix, y), xytext=(20, 20),
                textcoords="offset points",
                bbox={"boxstyle": "round", "fc": "w"},
                arrowprops={'arrowstyle': '->'},
                )
            fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('motion_notify_event', onclick)
plt.show()
