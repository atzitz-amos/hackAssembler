import numpy as np
from matplotlib import pyplot as plt

fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))

size = 0.3
vals = np.array([[55136., 129266.], [157390., 389104.], [76578., 203929.]])
# Normalize vals to 2 pi
valsnorm = vals / np.sum(vals) * 2 * np.pi
# Obtain the ordinates of the bar edges
valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)

cmap = plt.colormaps["tab20c"]
outer_colors = cmap(np.arange(3) * 4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

b1 = ax.bar(x=valsleft[:, 0],
            width=valsnorm.sum(axis=1), bottom=1 - size, height=size,
            color=outer_colors, edgecolor='w', linewidth=1, align="edge")

labels = ["Primarstufe 1-2", "Primarstufe 3-8", "Sekundarstufe I"]
handles = [plt.Rectangle((0, 0), 1, 1, color=outer_colors[label]) for label in range(3)]
ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(-0.1, 1.05))

b2 = ax.bar(x=valsleft.flatten(),
            width=valsnorm.flatten(), bottom=1 - 2 * size, height=size,
            color=inner_colors, edgecolor='w', linewidth=1, align="edge")

ax.annotate("Ausländer/innen [%]", xy=(-1.5, 0.6), xytext=(-1.8, 0.4),
            arrowprops=dict(arrowstyle="->"))

ax.annotate("Ausländer/innen [%]", xy=(1.6, 0.55), xytext=(0.2, 0.6), textcoords=ax,
            arrowprops=dict(arrowstyle="->"))

ax.annotate("Ausländer/innen [%]", xy=(0.2, 0.5), xytext=(0.75, 0.65), textcoords=ax,
            arrowprops=dict(arrowstyle="->"))

ax.annotate("Quelle: bfs.admin.ch", xy=(0.9, -0.1), xycoords=ax)

ax.set(title="Ausländeranteil nach Schulstufe")
ax.set_axis_off()
plt.savefig("d")
